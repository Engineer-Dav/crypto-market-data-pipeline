-- BRONZE STAGE 
CREATE TABLE crypto_market_raw(
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    coin_id VARCHAR(50),
    symbol  VARCHAR(50),
    name_   VARCHAR(50),
    current_price NUMERIC,
    market_cap    NUMERIC,
    market_cap_rank  SMALLINT,
    total_volume   NUMERIC,
    high_24h     NUMERIC,
    low_24h      NUMERIC,
    price_change_24h NUMERIC,
    price_change_percentage_24h NUMERIC,
    ath NUMERIC,
    ath_date TIMESTAMP,
    last_updated TIMESTAMP,
    ingestion_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
-- SILVER STAGE
CREATE TABLE dim_crypto_asset(
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    coin_id VARCHAR(50) UNIQUE NOT NULL,
    symbol  VARCHAR(50) NOT NULL,
    name_ VARCHAR(50) NOT NULL
);

CREATE TABLE fact_crypto_market(
    id  INTEGER  GENERATED ALWAYS AS IDENTITY PRIMARY KEY, 
    dim_id INTEGER NOT NULL,
    prices  NUMERIC NOT NULL,
    market_cap NUMERIC,
    market_cap_rank SMALLINT,
    total_volume NUMERIC NOT NULL,
    high_24h  NUMERIC,
    low_24h  NUMERIC,
    price_change_24h NUMERIC,
    price_change_percentage_24h NUMERIC,
    ath NUMERIC,
    ath_date TIMESTAMP,
    last_updated TIMESTAMP,
    ingestion_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(dim_id) REFERENCES dim_crypto_asset(id)
);
-- GOLD STAGE
CREATE TABLE gold_market_overview(
    coin_id VARCHAR(50) NOT NULL PRIMARY KEY,
    symbol VARCHAR(50) NOT NULL,
    name_ VARCHAR(50) NOT NULL,
    current_prices NUMERIC,
    market_cap NUMERIC,
    market_cap_rank SMALLINT,
    total_volume NUMERIC,
    price_change_percentage_24h NUMERIC,
    last_updated TIMESTAMP,
    refresh_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE gold_market_statistics(
    coin_id VARCHAR(50) NOT NULL PRIMARY KEY,
    symbol VARCHAR(50) NOT NULL,  
    name_ VARCHAR(50) NOT NULL,
    average_price NUMERIC,
    average_volume NUMERIC,
    highest_price NUMERIC,
    lowest_price NUMERIC,
    average_market_cap NUMERIC,
    price_volatility NUMERIC,
    refresh_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
