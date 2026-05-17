import requests
import json
import os
import logging

# Configure the logging engine
# This tells Python to save logs to 'pipeline.log' AND print them to the terminal screen
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("pipeline.log"),
        logging.StreamHandler()
    ]
)

def fetch_osm_data(city="London"):
    query = f"""
    [out:json];
    area[name="{city}"]->.searchArea;
    (node["amenity"="cafe"](area.searchArea););
    out body;
    """
    url = "https://overpass-api.de/api/interpreter"
    headers = {"User-Agent": "SpatialETLPipeline_PortfolioProject/1.0"}
    
    # Notice we changed print() to logging.info()
    logging.info(f"📡 Sending request to Overpass API for {city}...")
    
    try:
        response = requests.get(url, params={'data': query}, headers=headers, timeout=30)
        
        if response.status_code == 200:
            output_directory = "data/bronze"
            file_name = f"{city.lower()}_cafes_raw.json"
            full_path = os.path.join(output_directory, file_name)
            
            with open(full_path, "w") as f:
                json.dump(response.json(), f, indent=2)
                
            logging.info(f"✅ Success! Raw data saved to: {full_path}")
            
        else:
            # We use logging.error() for failures so they stand out in the log file
            logging.error(f"❌ Server returned status code {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        logging.error(f"❌ Connection Error: Could not reach the server. Details: {e}")

if __name__ == "__main__":
    fetch_osm_data()