import streamlit as st
import pandas as pd
from sqlalchemy import text
from db import get_engine

st.title("Crypto Analytics Dashboard")

engine = get_engine()

@st.cache_data
def load_data():
    query = """
    SELECT *
    FROM crypto_prices
    """
    with engine.connect() as conn:
        df = pd.read_sql(text(query), conn)
    return df

df = load_data()

if df.empty:
    st.warning("No data available")
else:
    st.subheader("Latest Crypto Prices")

    latest_df = df.sort_values("ingestion_time", ascending=False).drop_duplicates("crypto_id")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Coins Tracked", len(latest_df))
    col2.metric("Top Market Cap", f"${latest_df['market_cap'].max():,.0f}")
    col3.metric("Last Ingestion", latest_df['ingestion_time'].max())



    st.dataframe(latest_df[[
        "crypto_id", "symbol", "price_usd", "market_cap"
    ]])

    st.subheader("Price Trend")

    selected_crypto = st.selectbox(
        "Select Cryptocurrency",
        df["crypto_id"].unique()
    )

    filtered_df = df[df["crypto_id"] == selected_crypto].sort_values("ingestion_time")

    st.line_chart(filtered_df.set_index("ingestion_time")["price_usd"])