CREATE DATABASE crypto_db;

USE crypto_db;

CREATE TABLE crypto_prices (
    crypto_id VARCHAR(100) PRIMARY KEY,
    symbol VARCHAR(20),
    name VARCHAR(100),
    price_usd FLOAT,
    market_cap FLOAT,
    volume_24h FLOAT,
    last_updated DATETIME2
);

SELECT * FROM crypto_prices;

DROP TABLE IF EXISTS crypto_prices;

CREATE TABLE crypto_prices (
    crypto_id VARCHAR(100),
    symbol VARCHAR(20),
    name VARCHAR(100),
    price_usd FLOAT,
    market_cap FLOAT,
    volume_24h FLOAT,
    last_updated DATETIME2,
    
    ingestion_time DATETIME2 DEFAULT GETDATE(),

    CONSTRAINT pk_crypto PRIMARY KEY (crypto_id, ingestion_time)
);

SELECT TOP 20 * FROM crypto_prices;

CREATE TABLE etl_runs (
    run_id INT IDENTITY(1,1) PRIMARY KEY,
    start_time DATETIME2,
    end_time DATETIME2,
    status VARCHAR(20),
    records_processed INT,
    error_message VARCHAR(MAX)
);

SELECT * FROM etl_runs ORDER BY run_id DESC;

SELECT COUNT(*) FROM crypto_prices;

CREATE INDEX ix_crypto_prices_crypto_id ON crypto_prices(crypto_id);

CREATE INDEX ix_crypto_prices_last_updated ON crypto_prices(last_updated DESC);