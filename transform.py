import pandas as pd
import logging
from datetime import datetime, timezone

def transform_crypto_data(data : list) -> pd.DataFrame:
    if not data:
        logging.warning("No data received for transformation")
        return pd.DataFrame()
    
    df = pd.DataFrame(data)
    
    required_columns = [
        "id",
        "symbol",
        "name",
        "current_price",
        "market_cap",
        "total_volume",
        "last_updated"
    ]
    
    df = df[required_columns]
    
    df = df.rename(columns={
        "id" : "crypto_id",
        "current_price" : "price_usd",
        "total_volume" : "volume_24h"
    })
    
    df["ingestion_time"] = datetime.now(timezone.utc)
    df["last_updated"] = pd.to_datetime(df["last_updated"], errors="coerce")
    
    df = df.dropna(subset=["crypto_id","price_usd"])
    
    df["market_cap"] = df["market_cap"].fillna(0)
    df["volume_24h"] = df["volume_24h"].fillna(0)
    
    df = df.drop_duplicates(subset=["crypto_id"])

    logging.info(f"Transformed data shape: {df.shape}")

    return df

def filter_new_data(df : pd.DataFrame, latest_timestamp):
    
    df["last_updated"] = pd.to_datetime(df["last_updated"]).dt.tz_localize(None)

    if latest_timestamp is None:
        return df
    
    filtered_df = df[df["last_updated"] > latest_timestamp]
    
    logging.info(f"Filtered new records: {len(filtered_df)}")
    
    return filtered_df