# Harvard Art Museums Collection Explorer

## Overview
A Streamlit-based web application for exploring the Harvard Art Museums collection. Features an ETL pipeline that fetches data from the Harvard Art Museums API and stores it in a SQLite database, with 25+ SQL queries for data analysis and interactive visualizations.

## Current State
- Fully functional Streamlit application
- Uses Harvard Art Museums API (API key pre-configured)
- SQLite database for local data storage
- Interactive data collection, SQL queries, and visualizations

## Project Structure
- `app.py` - Main Streamlit application
- `harvard_artifacts.db` - SQLite database (created at runtime)

## Running the Application
The application runs via Streamlit on port 5000:
```bash
streamlit run app.py --server.port 5000 --server.address 0.0.0.0 --server.enableCORS false --server.enableXsrfProtection false --server.headless true
```

## Key Features
1. **Data Collection Tab** - Fetch artifacts from Harvard API by classification
2. **SQL Queries Tab** - 25+ predefined queries plus custom query editor
3. **Visualizations Tab** - Interactive charts using Plotly
4. **Stats Tab** - Database statistics and project progress

## Dependencies
- streamlit
- pandas
- plotly
- requests

## Database Schema
- `artifact_metadata` - Main artifact information
- `artifact_media` - Media/image counts
- `artifact_colors` - Color analysis data
