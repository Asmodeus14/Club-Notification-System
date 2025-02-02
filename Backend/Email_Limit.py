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


