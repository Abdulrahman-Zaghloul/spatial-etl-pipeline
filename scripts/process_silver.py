import json
import os
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

def transform_bronze_to_silver(city="London"):
    """
    Reads raw JSON data from Bronze, filters out anomalies, constructs 
    formal spatial geometry points, and saves a clean GeoJSON to Silver.
    """
    input_path = f"data/bronze/{city.lower()}_cafes_raw.json"
    output_path = f"data/silver/{city.lower()}_cafes_clean.geojson"
    
    print(f"🔄 Step 1: Loading raw Bronze data from {input_path}...")
    
    # 1. Load the raw JSON file
    if not os.path.exists(input_path):
        print(f"❌ Error: Cannot find Bronze file at {input_path}")
        return
        
    with open(input_path, "r") as f:
        data = json.load(f)
        
    # OpenStreetMap data returns a list of dictionaries inside the 'elements' key
    raw_elements = data.get("elements", [])
    print(f"📊 Found {len(raw_elements)} raw cafe records.")
    
    # 2. Parse JSON into structured lists
    cleaned_records = []
    
    for el in raw_elements:
        # Extract attributes safely using .get() to avoid crashing on missing data
        lat = el.get("lat")
        lon = el.get("lon")
        tags = el.get("tags", {})
        name = tags.get("name", "Unnamed Cafe") # Default text if name is blank
        
        # Data Quality Check: Skip records with missing coordinates
        if lat is None or lon is None:
            continue
            
        cleaned_records.append({
            "osm_id": el.get("id"),
            "name": name,
            "latitude": lat,
            "longitude": lon
        })
        
    # 3. Convert parsed list to a standard Pandas DataFrame
    df = pd.DataFrame(cleaned_records)
    
    print("🧠 Step 2: Creating spatial geometry point objects...")
    # 4. Transform Lat/Lon columns into formal Shapely 'Point' geometries
    geometry = [Point(xy) for xy in zip(df["longitude"], df["latitude"])]
    
    # 5. Build the GeoDataFrame and declare the Coordinate Reference System (CRS)
    # EPSG:4326 is the default standard for global latitude and longitude coordinates.
    gdf = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")
    
    # 6. Save refined dataset to the Silver Layer as a GeoJSON
    print(f"💾 Step 3: Saving clean spatial file to {output_path}...")
    gdf.to_file(output_path, driver="GeoJSON")
    print("✅ Success! Silver Layer layer is built and validated.")

if __name__ == "__main__":
    transform_bronze_to_silver()
