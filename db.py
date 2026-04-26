import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

def get_engine():
    server=os.getenv("DB_SERVER")
    database=os.getenv("DB_DATABASE")
    
    connection_string = (
        f"mssql+pyodbc://@{server}/{database}"
        "?driver=ODBC+Driver+17+for+SQL+Server"
        "&Trusted_Connection=yes"
        )
    
    engine = create_engine(connection_string, fast_executemany=True)

    return engine

engine = get_engine()
def get_latest_timestamp():
    
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT MAX(last_updated) FROM crypto_prices
        """))
        
        latest_time = result.scalar()

    return latest_time