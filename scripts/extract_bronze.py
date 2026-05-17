import requests
import json
import os

def fetch_osm_data(city="London"):
    """
    Connects to the OpenStreetMap Overpass API, requests cafe data 
    for a specific city, and saves the raw response to the Bronze layer.
    """
    
    query = f"""
    [out:json];
    area[name="{city}"]->.searchArea;
    (node["amenity"="cafe"](area.searchArea););
    out body;
    """
    
    url = "https://overpass-api.de/api/interpreter"
    
    # NEW CODE: Our custom "Name Tag" to bypass the 406 Bot Blocker
    headers = {
        "User-Agent": "SpatialETLPipeline_PortfolioProject/1.0"
    }
    
    print(f"📡 Step 1: Sending request to Overpass API for {city}...")
    
    try:
        # NEW CODE: We inject the headers into our request
        response = requests.get(url, params={'data': query}, headers=headers, timeout=30)
        
        if response.status_code == 200:
            
            output_directory = "data/bronze"
            file_name = f"{city.lower()}_cafes_raw.json"
            full_path = os.path.join(output_directory, file_name)
            
            with open(full_path, "w") as f:
                json.dump(response.json(), f, indent=2)
                
            print(f"✅ Step 2: Success! Raw data saved to: {full_path}")
            
        else:
            print(f"❌ Error: Server returned status code {response.status_code}")
            print(f"Server Response: {response.text}") # Added this just in case!
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection Error: Could not reach the server. Details: {e}")

if __name__ == "__main__":
    fetch_osm_data()