from fastapi import FastAPI, HTTPException, Path
from datetime import datetime
import json
import os

app = FastAPI(title="Regional Vegetable Market API")

@app.get("/api/v1/{place}/today")
def get_today_prices(
    place: str = Path(..., title="The name of the region, e.g., chennai")
):
    """
    Dynamically fetches today's vegetable prices for a specific region.
    """
    today_str = datetime.now().strftime("%d-%m-%Y")
    
    # Construct the expected file path
    file_path = os.path.join("data", today_str, f"{place.lower()}.json")
    
    # Check if the scraper has populated this directory yet
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=404, 
            detail=f"Price data not found for {place} on {today_str}."
        )
    
    # Load and return the targeted JSON file
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
        
    return {"status": "success", "region": place, "date": today_str, "data": data}