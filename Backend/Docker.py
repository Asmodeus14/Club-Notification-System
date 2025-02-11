import os
import time
import json
import logging
import dramatiq
from dramatiq.brokers.redis import RedisBroker
from redis import Redis
import sib_api_v3_sdk
from sib_api_v3_sdk import TransactionalEmailsApi, SendSmtpEmail
from sib_api_v3_sdk.rest import ApiException
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv(r"API.env")
api_key = os.getenv("BREVO_API_KEY")

# Configure Redis client (ensure connection parameters match your Docker setup)
redis_client = Redis(host="localhost", port=6379, db=0)

# Optionally, set up the Dramatiq broker (if not already configured elsewhere)
broker = RedisBroker(client=redis_client)
dramatiq.set_broker(broker)

def set_lock(key, value="1", ex=120):
    """
    Atomically set a lock key in Redis with an expiration.
    Returns True if the lock was acquired, False otherwise.
    """
    # Using the Redis SET command with NX ensures that the key is set only if it doesn't exist.
    return redis_client.set(key, value, ex=ex, nx=True)

@dramatiq.actor(max_retries=3)
def send_single_email(to_email, subject, content, use_lock=True):
    lock_key = f"email_lock:{to_email}"

    # Prevent the main process from executing this worker logic.
    if os.getpid() == os.getppid():
        logger.warning(f"Main process detected (PID: {os.getpid()}), skipping execution.")
        return

    if use_lock:
        # Try to acquire the lock atomically.
        if not set_lock(lock_key):
            logger.warning(f"Email to {to_email} is already being processed. Skipping.")
            return

    try:
        # Configure Brevo (Sendinblue) API client.
        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key['api-key'] = api_key
        api_instance = TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

        # Define sender and recipient.
        sender = {"name": "SRMU Club Notices", "email": "srmu.clubnotices@gmail.com"}
        recipient = [{"email": to_email, "name": to_email}]

        # Create the email object.
        send_smtp_email = SendSmtpEmail(
            sender=sender,
            to=recipient,
            html_content=content,
            subject=subject
        )

        # Send the email.
        api_instance.send_transac_email(send_smtp_email)
        logger.info(f"Email sent to {to_email} with subject '{subject}'")

    except ApiException as e:
        logger.error(f"Failed to send email to {to_email}: {e.reason}")
        # Raising Retry causes Dramatiq to requeue the message.
        raise dramatiq.Retry()
    finally:
        # Always clear the lock after processing.
        redis_client.delete(lock_key)

@dramatiq.actor
def send_bulk_emails(emails, subject, content):
    """
    Queue multiple emails for processing.
    Expects emails to be a list of dictionaries with an "email" key.
    """
    # Deduplicate by extracting unique email addresses.
    unique_emails = list({email_dict["email"] for email_dict in emails})

    for email in unique_emails:
        # Check if the email is not already locked.
        if not redis_client.exists(f"email_lock:{email}"):
            # When sending bulk emails, we bypass the per-task lock check inside send_single_email.
            send_single_email.send(email, subject, content, use_lock=False)
        else:
            logger.warning(f"Skipping {email} (already queued/processing)")
    
    logger.info(f"Queued {len(unique_emails)} unique emails for sending.")

# Constants for the queue and daily limit.
QUEUE_NAME = "email_queue"
DAILY_LIMIT = 220  # Example daily limit

@dramatiq.actor
def process_email_queue():
    """
    Process emails from the Redis queue up to a daily limit.
    Each queue item is assumed to be a JSON string with keys: "email", "subject", "content".
    """
    count = 0

    while count < DAILY_LIMIT:
        email_data = redis_client.lpop(QUEUE_NAME)
        if not email_data:
            logger.info("No more emails to send today.")
            break  # Stop if the queue is empty
        
        try:
            # Deserialize the JSON string from bytes.
            email_info = json.loads(email_data.decode('utf-8'))
            email_list = email_info["email"]
            subject = email_info["subject"]
            content = email_info["content"]
        except (json.JSONDecodeError, KeyError) as err:
            logger.error(f"Error decoding queue data: {err}")
            continue

        logger.info(f"Processing email(s): {email_list}")
        
        # Queue the bulk send process.
        send_bulk_emails.send(email_list, subject, content)
        count += 1
        # Sleep briefly to help avoid API rate limits.
        time.sleep(1)

    logger.info(f"Processed {count} emails today.")
    
# from flask_socketio import SocketIO, emit

@dramatiq.actor
def send_notification(user_id, message):
    from Backend.Test import socketio
    # Simulate a background process delay
    time.sleep(2)
    
    socketio.emit('notification', {'user_id': user_id, 'message': message})
    print(f"Notification sent to user {user_id}: {message}")

# queued_emails = redis_client.lrange(QUEUE_NAME, 0, -1)
# print(f"Emails in the queue: {queued_emails}")