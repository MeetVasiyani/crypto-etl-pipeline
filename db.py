import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

_engine = None

def get_engine():
    global _engine
    
    if _engine is None:
        server = os.getenv("DB_SERVER")
        database = os.getenv("DB_DATABASE")

        connection_string = (
            f"mssql+pyodbc://@{server}/{database}"
            "?driver=ODBC+Driver+17+for+SQL+Server"
            "&Trusted_Connection=yes"
        )

        _engine = create_engine(connection_string, fast_executemany=True)

    return _engine


def get_latest_timestamp():
    engine = get_engine()
    
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT MAX(last_updated) FROM crypto_prices
        """))
        
        latest_time = result.scalar()

    return latest_time