import os
import time
import json
import requests
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()
api_token = os.getenv("BRIGHT_DATA_API_TOKEN")
collection_id = os.getenv("COLLECTOR_ID")

if not api_token:
    raise ValueError("API Token not found. Please check your .env file.")

# Endpoints and Headers
trigger_url = f"https://api.brightdata.com/dca/trigger?collector={collection_id}"
headers = {
    "Authorization": f"Bearer {api_token}",
    "Content-Type": "application/json"
}
payload = [{"url": "https://vegetablemarketprice.com/market/chennai/today"}]

# --- STEP 1: Trigger the Scraper ---
print("Triggering the scraper...")
trigger_response = requests.post(trigger_url, headers=headers, json=payload)
trigger_response.raise_for_status() # Fails immediately if the token is invalid

# Extract the job ID from the response
collection_id = trigger_response.json().get("collection_id")
print(f"Job triggered successfully. Collection ID: {collection_id}")


# --- STEP 2: Poll the Dataset Endpoint ---
dataset_url = f"https://api.brightdata.com/dca/dataset?id={collection_id}"
auth_header_only = {"Authorization": f"Bearer {api_token}"}

max_retries = 15
retry_interval = 10 # Wait 10 seconds between checks to be time-efficient

print("Polling for results...")

for attempt in range(1, max_retries + 1):
    # Fetch the dataset status
    dataset_response = requests.get(dataset_url, headers=auth_header_only)
    
    if dataset_response.status_code == 200:
        # A 200 status means the job is done and the data is attached
        print("Data retrieved successfully!")
        
        # Parse and save the data efficiently to disk
        data = dataset_response.json()
        filename= f"chennai_vegetables_{datetime.now().strftime('%d-%m-%Y')}.json"
        with open(filename, "w", encoding="utf-8") as file:
            # ensure_ascii=False ensures Tamil characters are written correctly
            json.dump(data, file, indent=2, ensure_ascii=False)
            
        print(f"Data saved to {filename}")
        break
        
    elif dataset_response.status_code == 202:
        # A 202 status means the job is still processing
        print(f"[Attempt {attempt}/{max_retries}] Job still processing... waiting {retry_interval}s.")
        time.sleep(retry_interval)
        
    else:
        # Handle unexpected errors (e.g., 404, 500)
        print(f"Failed to fetch data. Status: {dataset_response.status_code}")
        print(dataset_response.text)
        break
else:
    # This block executes if the loop finishes without breaking (max retries hit)
    print("Max retries reached. The job took too long to complete.")