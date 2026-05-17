# End-to-End Spatial ETL Pipeline (London Cafe Density Analysis)

A production-grade, three-tiered data engineering pipeline that ingests, cleans, processes, and visualizes geographic data from the OpenStreetMap (OSM) API. Built entirely on Ubuntu Linux using Python and a virtualized Medallion Architecture workflow.

## 🏗️ System Architecture

This project implements a classic enterprise **Medallion Architecture** to isolate data processing stages:

> **[Overpass API]** ──(Ingest Raw JSON)──> **[Bronze Layer: Raw Data]** > ──(Spatial Quality Filter)──> **[Silver Layer: Cleaned GeoJSON]** > ──(Mathematical Binning)──> **[Gold Layer: Aggregated Density]** > ──(Folium Engine Render)──> **[Interactive HTML Heatmap]**

* **Bronze Layer (`data/bronze/`)**: Ingests raw, nested JSON payloads directly from the Overpass API via coordinate querying.
* **Silver Layer (`data/silver/`)**: Parses raw elements, extracts spatial geometries, applies a strict geographic bounding box filter, and structuralizes data into validated GeoJSON using `geopandas`.
* **Gold Layer (`data/gold/`)**: Executes data binning by rounding coordinates to 2 decimal places (creating ~1.1km x 1.1km zones) and aggregating data into a competitive density matrix (`.csv`).
* **Visualization Layer (`data/visualizations/`)**: Translates Gold metrics into an interactive LeafletJS-powered spatial heatmap (`.html`) for business intelligence.

## 🚀 Key Engineering Features

* **Centralized Production Logging**: Replaced standard out print statements with Python's native `logging` library. All pipeline states, row counts, API latency metrics, and errors are captured sequentially into a single `pipeline.log` file with exact timestamps.
* **Master Automation Orchestrator**: Developed a central master script (`run_pipeline.py`) that executes steps as sub-processes, monitors execution runtimes, and features defensive error handling to safely halt downstream processes upon upstream script failure.
* **Defensive Spatial Data Engineering**: Encountered a data quality anomaly where matching boundary names pulled a rogue cluster in northern Scandinavia. Engineered a coordinate-based bounding box filter inside the Silver tier (`49.0 <= lat <= 61.0` and `-8.0 <= lon <= 2.0`) to instantly drop geographical noise and guarantee dataset integrity.

## 🛠️ Technology Stack
* **OS**: Ubuntu Linux 
* **Language**: Python 3 (Virtual Environment managed)
* **Libraries**: GeoPandas, Pandas, Folium, Shapely, Requests
* **Orchestration**: Python Subprocess Engine
* **Version Control**: Git / GitHub

## 📊 Pipeline Observability & Output

### Automated Execution Logs
```text
2026-05-17 22:36:37,576 - INFO -  Success! Gold Layer is complete and ready for business analysis.
2026-05-17 22:36:37,631 - INFO -  [Orchestrator] Step completed successfully: scripts/aggregate_gold.py
2026-05-17 22:36:37,631 - INFO -  [Orchestrator] Starting execution step: scripts/visualize_map.py
2026-05-17 22:36:38,114 - INFO -  Interactive heatmap saved successfully to: data/visualizations/london_cafe_heatmap.html
2026-05-17 22:36:38,179 - INFO -  [Orchestrator] Step completed successfully: scripts/visualize_map.py
2026-05-17 22:36:38,179 - INFO -  ==================== PIPELINE EXECUTION COMPLETE IN 4.95s ====================