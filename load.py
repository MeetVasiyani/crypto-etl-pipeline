import logging
import pandas as pd
from sqlalchemy import text,types
from db import get_engine
from datetime import datetime, timezone

def load_data(df : pd.DataFrame):
    if df.empty:
        logging.warning("Empty Dataframe. Skipping load.")
        return
    
    engine = get_engine()
    
    staging_table = "crypto_prices_staging"
    
    try:
        with engine.begin() as conn:
            df.to_sql(
                staging_table,
                con=conn,
                if_exists="replace",
                index=False,
                dtype={
                    "crypto_id": types.VARCHAR(100),
                    "symbol": types.VARCHAR(20),
                    "name": types.VARCHAR(100),
                    "price_usd": types.FLOAT(),
                    "market_cap": types.FLOAT(),
                    "volume_24h": types.FLOAT(),
                    "last_updated": types.DateTime()
                }
            )
            
            logging.info("Data loaded into staging table.")
            
            append_query = f"""
            INSERT INTO crypto_prices (
                crypto_id, symbol, name, price_usd,
                market_cap, volume_24h, last_updated, ingestion_time
            )
            SELECT 
                crypto_id, symbol, name, price_usd,
                market_cap, volume_24h, last_updated, ingestion_time
            FROM {staging_table};
            """
            
            conn.execute(text(append_query))
            
            logging.info(f"Appended {len(df)} new records to crypto_prices")
            
    except Exception as e:
        logging.error(f"Error during load {e}")
        raise

def start_pipeline_run():
    engine = get_engine()
    
    with engine.begin() as conn:
        result = conn.execute(text("""
            INSERT INTO etl_runs (start_time,status)
            OUTPUT INSERTED.run_id
            VALUES (:start_time, :status)
        """),{
            "start_time": datetime.now(timezone.utc),
            "status" : "RUNNING"
        })
        
        run_id = result.fetchone()[0]
        return run_id
    

def end_pipeline_run(run_id, status, records_processed=0, error_message=None):
    engine = get_engine()
    
    with engine.begin() as conn:
        conn.execute(text("""
            UPDATE etl_runs
            SET end_time = :end_time,
                status = :status,
                records_processed = :records_processed,
                error_message = :error_message
            WHERE run_id = :run_id
        """),{
            "end_time": datetime.now(timezone.utc),
            "status": status,
            "records_processed": records_processed,
            "error_message": error_message,
            "run_id": run_id
        })