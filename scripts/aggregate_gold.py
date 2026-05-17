
import geopandas as gpd
import os

def create_gold_aggregation(city="London"):
    """
    Reads clean spatial data from Silver, performs spatial grid binning
    by rounding coordinates, aggregates counts, and outputs a Gold business layer.
    """
    input_path = f"data/silver/{city.lower()}_cafes_clean.geojson"
    output_path = f"data/gold/{city.lower()}_cafe_density.csv"
    
    print(f"🥇 Step 1: Loading clean Silver layer from {input_path}...")
    
    # 1. Safety check: make sure Silver data actually exists
    if not os.path.exists(input_path):
        print(f"❌ Error: Cannot find Silver file at {input_path}")
        return
        
    gdf = gpd.read_file(input_path)
    
    print("🧮 Step 2: Executing spatial binning logic...")
    
    # 2. Mathematical Rounding Trick
    # By rounding the lat/lon to 2 decimal places, we create artificial 
    # geographic grid blocks (roughly 1.1 km x 1.1 km zones).
    gdf['grid_lat'] = gdf['latitude'].round(2)
    gdf['grid_lon'] = gdf['longitude'].round(2)
    
    # 3. The Group-By Aggregation
    # We group by our new grid squares and count how many cafes share that grid cell.
    density_df = gdf.groupby(['grid_lat', 'grid_lon']).size().reset_index(name='cafe_count')
    
    # 4. Sort the results so the heaviest competitor clusters are at the very top
    density_df = density_df.sort_values(by='cafe_count', ascending=False)
    
    # 5. Output the final refined business table to Gold as a clean CSV
    print(f"💾 Step 3: Exporting Gold business intelligence layer to {output_path}...")
    
    # Ensure the gold directory exists just in case
    os.makedirs("data/gold", exist_ok=True)
    
    density_df.to_csv(output_path, index=False)
    
    print("📊 Top 5 Highest Density Competitor Clusters:")
    print(density_df.head(5).to_string(index=False))
    print("\n✅ Success! Gold Layer is complete and ready for business analysis.")

if __name__ == "__main__":
    create_gold_aggregation()