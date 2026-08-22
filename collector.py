import os
import requests
from dotenv import load_dotenv

# Load variables from the .env file into the script's environment
load_dotenv()

# Retrieve the token
api_token = os.getenv("BRIGHT_DATA_API_TOKEN")

# Fail early if the token is missing
if not api_token:
    raise ValueError("API Token not found. Please check your .env file.")

# 1. Define the endpoint URL
url = "https://api.brightdata.com/dca/trigger?collector=c_mt3964fg23qhketpko"

# 2. Set headers using an f-string to inject the secure token
headers = {
    "Authorization": f"Bearer {api_token}",
    "Content-Type": "application/json"
}

# 3. Define the payload
payload = [
    {
        "url": "https://vegetablemarketprice.com/market/chennai/today"
    }
]

# 4. Make the POST request
response = requests.post(url, headers=headers, json=payload)

# 5. Output the results
print(f"Status Code: {response.status_code}")

if response.ok:
    print("Response Data:")
    print(response.json())
else:
    print(f"Error: {response.text}")