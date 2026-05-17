
import pandas as pd
import folium
from folium.plugins import HeatMap
import os
import logging

# Hook into our centralized logging architecture
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("pipeline.log"),
        logging.StreamHandler()
    ]
)

def generate_heatmap(city="London"):
    input_path = f"data/gold/{city.lower()}_cafe_density.csv"
    output_dir = "data/visualizations"
    output_path = os.path.join(output_dir, f"{city.lower()}_cafe_heatmap.html")
    
    logging.info(f"🗺️ Loading Gold aggregation data from {input_path}...")
    
    if not os.path.exists(input_path):
        logging.error(f"❌ Error: Gold data file not found at {input_path}")
        return
        
    df = pd.read_csv(input_path)
    
    # Folium's HeatMap plugin expects a list of points formatted as [lat, lon, weight]
    logging.info("🎨 Preparing coordinates for heat layer map rendering...")
    heat_data = df[['grid_lat', 'grid_lon', 'cafe_count']].values.tolist()
    
    # Initialize the interactive leaflet map centered over central London
    logging.info("📌 Generating base map layer...")
    base_map = folium.Map(location=[51.5074, -0.1278], zoom_start=12, tiles="CartoDB positron")
    
    # Construct the heatmap overlay and bind it to our base map
    HeatMap(heat_data, radius=15, blur=10, max_zoom=13).add_to(base_map)
    
    # Ensure our visualization destination folder exists
    os.makedirs(output_dir, exist_ok=True)
    base_map.save(output_path)
    logging.info(f"💾 Interactive heatmap saved successfully to: {output_path}")

if __name__ == "__main__":
    generate_heatmap()