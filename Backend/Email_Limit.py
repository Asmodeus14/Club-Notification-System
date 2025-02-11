import requests

def check_brevo_email_quota(api_key):
    headers = {
        "accept": "application/json",
        "api-key": api_key
    }
    
    # Send request to Brevo API
    response = requests.get("https://api.brevo.com/v3/account", headers=headers)

    # Check if the response is successful
    if response.status_code == 200:
        data = response.json()

        # # Print the formatted JSON response
        # print("Response Data (Prettified):")
        # print(json.dumps(data, indent=4))  # Prettify the dictionary with indentation
        
        # Extract credits information from the plan list
        plan_data = data.get("plan", [])
        credits_used = None
        

        # Look for the "sendLimit" plan type (marketing email limit)
        for plan in plan_data:
            if plan.get("creditsType") == "sendLimit":
                credits_used = plan.get("credits", "N/A")
                break

        return credits_used
    else:
        # Return error if the API request fails
        return f"Error: {response.json()}"

import redis
import json
from datetime import datetime
from Docker import process_email_queue
# Connect to Redis
redis_client = redis.Redis(host='localhost', port=6379, db=0)

QUEUE_NAME = "email_queue"

def add_to_email_queue(email, subject, content):
    """Add email to Redis queue."""
    email_data = {
        "email": email,
        "subject": subject,
        "content": content,
        "timestamp": datetime.now().isoformat()
    }
    redis_client.rpush(QUEUE_NAME, json.dumps(email_data))
    print(f"📌 Queued email for {email}")
    process_email_queue()
    
    
# queued_emails = redis_client.lrange(QUEUE_NAME, 0, -1)
# print(f"Emails in the queue: {queued_emails}")

