# app.py
from dramatiq.brokers.redis import RedisBroker
from redis import Redis
import dramatiq
import sib_api_v3_sdk
from sib_api_v3_sdk import TransactionalEmailsApi, SendSmtpEmail
from sib_api_v3_sdk.rest import ApiException
import os
from dotenv import load_dotenv
import time 
import json

load_dotenv(r"API.env")

global api_key 
api_key=os.getenv("BREVO_API_KEY")
# Configure Dramatiq to use Redis
redis_client = Redis(host="localhost", port=6379, db=0)

@dramatiq.actor(max_retries=3)
def send_single_email( to_email, subject, content,use_lock=True):
    lock_key = f"email_lock:{to_email}"
    
    if os.getpid() == os.getppid():  # Prevents main process from executing
        print(f"⚠️ Main process detected (PID: {os.getpid()}), skipping execution.")
        return
    lock_key = f"email_lock:{to_email}"
    
    if use_lock and redis_client.exists(lock_key):
        print(f"⚠️ Email to {to_email} is already being processed. Skipping.")
        return
    if use_lock:
        redis_client.set(lock_key, "1", ex=120)
    
    # Set a lock (expires in 2 minutes)
    redis_client.set(lock_key, "1", ex=120)

    try:
        # Configure Brevo API
        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key['api-key'] = api_key
        api_instance = TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

        # Define sender & recipient
        sender = {"name": "SRMU Club Notices", "email": "srmu.clubnotices@gmail.com"}
        to = [{"email": to_email, "name": to_email}]

        # Create email object
        send_smtp_email = SendSmtpEmail(
            sender=sender,
            to=to,
            html_content=content,
            subject=subject
        )

        # Send email
        api_instance.send_transac_email(send_smtp_email)
        print(f"✅ Email sent to {to_email}")

    except ApiException as e:
        print(f"❌ Failed to send to {to_email}: {e.reason}")
        raise dramatiq.Retry()

    finally:
        redis_client.delete(lock_key)  # Release lock after sending


@dramatiq.actor
def send_bulk_emails( emails, subject, content):
    """Queue multiple emails for processing, ensuring each email is queued only once."""
    unique_emails = list({email_dict["email"] for email_dict in emails})

    for email in unique_emails:
        lock_key = f"email_lock:{email}"
        if not redis_client.exists(lock_key):  # Only queue if no lock exists
            send_single_email.send( email, subject, content,False)
        else:
            print(f"⚠️ Skipping {email} (already queued/processing)")
    
    print(f"✅ Queued {len(unique_emails)} unique emails for sending.")

QUEUE_NAME = "email_queue"
DAILY_LIMIT = 220  # Brevo's daily limit

@dramatiq.actor
def process_email_queue():
    """Process emails from Redis queue within Brevo's daily limit."""
    count = 0

    while count < DAILY_LIMIT:
        email_data = redis_client.lpop(QUEUE_NAME)
        if not email_data:
            print("✅ No more emails to send today.")
            break  # Stop if queue is empty
        
        # Deserialize the byte data from Redis
        email_info = json.loads(email_data.decode('utf-8'))  # decode from bytes and load JSON
        
        # Ensure email_info is correctly structured
        email_list = email_info["email"]  # Get the list of emails (you can loop through it for bulk sending)
        subject = email_info["subject"]
        content = email_info["content"]

        # Log email for debugging
        print(f"Processing email: {email_list}")
        
        send_bulk_emails.send(email_list, subject, content)
        count += 1
        time.sleep(1)  # Avoid hitting API rate limits

    print(f"✅ Processed {count} emails today.")
    
