# Crypto ETL Pipeline

An automated ETL pipeline that ingests real-time cryptocurrency data 
from the CoinGecko API, stores it in SQL Server, and visualizes it 
via a Streamlit dashboard.

## Architecture
- **Extract** — Fetches top 100 coins from CoinGecko API with retry logic
- **Transform** — Cleans, renames, and filters already-ingested records
- **Load** — Appends new records to SQL Server via a staging table
- **Dashboard** — Streamlit app showing KPIs, price trends, and market cap

## Setup
1. Create a virtual environment and run `pip install -r requirements.txt`
2. Copy `.env.example` to `.env` and fill in your DB credentials
3. Run the pipeline: `python etl.py`
4. Launch the dashboard: `streamlit run app.py`