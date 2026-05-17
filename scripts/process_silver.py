import json
import os
import logging
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

# Configure the logging engine to append to our central log file
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("pipeline.log"),
        logging.StreamHandler()
    ]
)

def transform_bronze_to_silver(city="London"):
    input_path = f"data/bronze/{city.lower()}_cafes_raw.json"
    output_path = f"data/silver/{city.lower()}_cafes_clean.geojson"
    
    logging.info(f"🔄 Loading raw Bronze data from {input_path}...")
    
    if not os.path.exists(input_path):
        logging.error(f"❌ Error: Cannot find Bronze file at {input_path}")
        return
        
    with open(input_path, "r") as f:
        data = json.load(f)
        
    raw_elements = data.get("elements", [])
    logging.info(f"📊 Found {len(raw_elements)} raw cafe records.")
    
    cleaned_records = []
    for el in raw_elements:
        lat = el.get("lat")
        lon = el.get("lon")
        tags = el.get("tags", {})
        name = tags.get("name", "Unnamed Cafe")
        
        if lat is None or lon is None:
            continue
            
        # 🛡️ SPATIAL DATA QUALITY FILTER: Drop any rogue points outside the UK boundary
        if not (49.0 <= lat <= 61.0 and -8.0 <= lon <= 2.0):
            continue
            
        cleaned_records.append({
            "osm_id": el.get("id"),
            "name": name,
            "latitude": lat,
            "longitude": lon
        })
        
    df = pd.DataFrame(cleaned_records)
    
    logging.info("🧠 Creating spatial geometry point objects...")
    geometry = [Point(xy) for xy in zip(df["longitude"], df["latitude"])]
    
    gdf = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")
    
    logging.info(f"💾 Saving clean spatial file to {output_path}...")
    gdf.to_file(output_path, driver="GeoJSON")
    logging.info("✅ Success! Silver Layer is built and validated.")

if __name__ == "__main__":
    transform_bronze_to_silver()