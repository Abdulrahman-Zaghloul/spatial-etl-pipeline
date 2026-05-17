import geopandas as gpd
import os
import logging

# Configure logging to append to our central log file
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("pipeline.log"),
        logging.StreamHandler()
    ]
)

def create_gold_aggregation(city="London"):
    input_path = f"data/silver/{city.lower()}_cafes_clean.geojson"
    output_path = f"data/gold/{city.lower()}_cafe_density.csv"
    
    logging.info(f"🥇 Loading clean Silver layer from {input_path}...")
    
    if not os.path.exists(input_path):
        logging.error(f"❌ Error: Cannot find Silver file at {input_path}")
        return
        
    gdf = gpd.read_file(input_path)
    
    logging.info("🧮 Executing spatial binning logic...")
    gdf['grid_lat'] = gdf['latitude'].round(2)
    gdf['grid_lon'] = gdf['longitude'].round(2)
    
    density_df = gdf.groupby(['grid_lat', 'grid_lon']).size().reset_index(name='cafe_count')
    density_df = density_df.sort_values(by='cafe_count', ascending=False)
    
    logging.info(f"💾 Exporting Gold business intelligence layer to {output_path}...")
    os.makedirs("data/gold", exist_ok=True)
    density_df.to_csv(output_path, index=False)
    
    logging.info("📊 Top 5 Highest Density Competitor Clusters:")
    # Loop through the dataframe printout so it renders cleanly in the logging stream
    for line in density_df.head(5).to_string(index=False).split('\n'):
        logging.info(f"  {line}")
        
    logging.info("✅ Success! Gold Layer is complete and ready for business analysis.")

if __name__ == "__main__":
    create_gold_aggregation()