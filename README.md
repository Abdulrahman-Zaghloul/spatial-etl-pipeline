
# End-to-End Spatial Data Engineering Pipeline

A production-focused geospatial ETL (Extract, Transform, Load) pipeline built to demonstrate scalable spatial data engineering principles on Linux.

This project simulates a high-value business case: automating the collection, cleaning, and structuring of location intelligence data (competitor coffee shops in London) to drive commercial real estate and market analysis decisions.

## 🏗️ Data Flow Architecture: The Medallion Framework
To ensure absolute data integrity, the pipeline isolates processes into three clear layers:

1. **Bronze Layer (Raw Ingestion):** * Script: `scripts/extract_bronze.py`
   * Action: Connects to the OpenStreetMap Overpass API and downloads raw JSON payloads. Implements custom User-Agent headers to bypass automated anti-bot security blocks (HTTP 406 errors).
   
2. **Silver Layer (Spatial Refining):**
   * Script: `scripts/process_silver.py`
   * Action: Reads raw JSON, drops invalid records missing coordinate data, parses attributes, and uses **GeoPandas** to construct formal spatial point geometry mapped to the universal global GPS standard (**EPSG:4326**). Outputs clean GeoJSON files.

3. **Gold Layer (Business Intelligence):**
   * Script: `scripts/aggregate_gold.py`
   * Action: Implements custom **Spatial Binning** logic by rounding geographic coordinates to two decimal places. This mathematically segments London into localized grid zones (~1.1km x 1.1km). It then aggregates the 4,747 records using a structured `groupby` count to expose the densest competitor clusters and locate market "dead zones" for business intelligence. Outputs a refined CSV dataset.
   
## 🛠️ Tech Stack & Skills Demonstrated
* **Operating System:** Ubuntu Linux Environment
* **Language/Libraries:** Python 3, Requests, Pandas, GeoPandas, Shapely
* **Architecture:** Three-tier Medallion Architecture (Bronze ➡️ Silver ➡️ Gold)
* **Version Control:** Git & GitHub Best Practices (Atomic Commits, Credential Caching)