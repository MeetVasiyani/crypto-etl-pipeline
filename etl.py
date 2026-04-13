import logging
import os

from db import get_latest_timestamp

from extract import fetch_all_crypto_data
from transform import transform_crypto_data, filter_new_data
from load import load_data, start_pipeline_run, end_pipeline_run

def setup_logging():
    os.makedirs("logs",exist_ok=True)
    
    logging.basicConfig(
        filename="logs/pipeline.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

if __name__ == "__main__":
    setup_logging()
    
    run_id = start_pipeline_run()
    
    try:
        logging.info(f"Pipeline started - Run ID: {run_id}")
        
        raw_data = fetch_all_crypto_data(pages=2)
        latest_timestamp = get_latest_timestamp()
        df = transform_crypto_data(raw_data)
        df = filter_new_data(df, latest_timestamp)
        load_data(df)
        
        end_pipeline_run(
            run_id=run_id,
            status="SUCCESS",
            records_processed=len(df)
        )
        
        logging.info("ETL pipeline completed successfully")
        print("Pipeline completed successfully")
        
    except Exception as e:
        logging.exception(f"Pipeline failed")
        
        end_pipeline_run(
            run_id=run_id,
            status="FAILED",
            records_processed=0,
            error_message=str(e)
        )
        
        print("Pipeline failed. Check logs.")
