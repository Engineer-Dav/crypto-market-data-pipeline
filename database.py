import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
from logger import logger
load_dotenv()

def get_connection():
    try:
        connection = psycopg2.connect(
            dbname = os.getenv("DB_NAME"),
            user = os.getenv("DB_USER"),
            password = os.getenv("DB_PASSWORD"),
            host = os.getenv("DB_HOST"),
            port = os.getenv("DB_PORT")
        )
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        logger.info("Connected to database successfully")
        return connection,cursor
    except psycopg2.Error as e:
        logger.error(f"Database connection error: {e}")
        return None,None
        
def insert_bronze_data(data):
    if not data:
        logger.warning("No data to insert into bronze, skipping")
        return
    connection, cursor = None, None
    try:
        connection, cursor = get_connection()
        if connection is None or cursor is None:
            logger.warning("Could not connect to database, aborting insert")
            return
        else:
            for coin in data:
                cursor.execute("""INSERT INTO crypto_market_raw(
                    coin_id,
                    symbol,
                    name_,
                    current_price,
                    market_cap,
                    market_cap_rank,
                    total_volume,
                    high_24h,
                    low_24h,
                    price_change_24h,
                    price_change_percentage_24h,
                    ath,ath_date,
                    last_updated) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                    (coin["id"],coin["symbol"],coin["name"],coin["current_price"],coin["market_cap"],coin["market_cap_rank"],
                    coin["total_volume"],
                    coin["high_24h"],coin["low_24h"],coin["price_change_24h"],coin["price_change_percentage_24h"],
                    coin["ath"],
                    coin["ath_date"],coin["last_updated"])
                    )
            connection.commit()
            logger.info("Data loaded to bronze successfully")
    except psycopg2.Error as e:
        logger.error(f"Database error: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def extract_bronze_data():
    connection, cursor = None, None
    try:
        connection,cursor = get_connection()
        if connection is None or cursor is None:
            logger.warning("Could not connect to database, aborting extract from Bronze")
            return
        cursor.execute("SELECT * FROM crypto_market_raw")
        data = cursor.fetchall()
        logger.info("Data extracted from bronze successfully")
        return data
    except psycopg2.Error as e:
        logger.error(f"Database Error: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def insert_silver_data(data):
    if data.empty:
        logger.warning("No data to insert into silver, skipping")
        return
    connection, cursor = None, None
    try:
        connection,cursor = get_connection()
        if connection is None or cursor is None:
            logger.warning("Could not connect to database, aborting insert to Silver")
            return
        for coins in data.to_dict("records"):
            cursor.execute("""INSERT INTO dim_crypto_asset (coin_id, symbol, name_)
                            VALUES (%s, %s, %s)
                            ON CONFLICT (coin_id)
                            DO UPDATE
                            SET
                            symbol = EXCLUDED.symbol,
                            name_ = EXCLUDED.name_;""",(
                            coins["coin_id"],
                            coins["symbol"],
                            coins["name_"]
                            ) )
            cursor.execute("SELECT id FROM dim_crypto_asset WHERE coin_id = %s",(coins["coin_id"],))
            dim_id =cursor.fetchone()["id"]
            cursor.execute("""INSERT INTO fact_crypto_market(
                           dim_id,
                           prices,
                           market_cap,
                           market_cap_rank,
                           total_volume,
                           high_24h,
                           low_24h,
                           price_change_24h,
                           price_change_percentage_24h,
                           ath,
                           ath_date,
                           last_updated) VALUES(
                           %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                            (dim_id,coins["current_price"],coins["market_cap"],
                            coins["market_cap_rank"],coins["total_volume"],
                            coins["high_24h"],coins["low_24h"],coins["price_change_24h"],
                            coins["price_change_percentage_24h"],coins["ath"],coins["ath_date"],
                            coins["last_updated"]))
        connection.commit()
        logger.info("Data loaded to silver successfully")    
    except psycopg2.Error as e:
        logger.error(f"Database Error: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
        
def insert_gold_market_overview():
    connection, cursor = None, None
    try:
        connection, cursor = get_connection()
        if connection is None or cursor is None:
            logger.warning("Could not connect to database, aborting insert to Gold overview")
            return
        cursor.execute("""INSERT INTO gold_market_overview(
                       coin_id,
                       symbol,
                       name_,
                       current_prices,
                       market_cap,
                       market_cap_rank,
                       total_volume,
                       price_change_percentage_24h,
                       last_updated) 
                       SELECT DISTINCT ON(coin_id)
                           coin_id,
                           symbol,
                           name_, 
                           prices,
                           market_cap,
                           market_cap_rank,
                           total_volume,
                           price_change_percentage_24h,
                           last_updated 
                        FROM dim_crypto_asset 
                        JOIN fact_crypto_market ON dim_crypto_asset.id =
                        fact_crypto_market.dim_id
                        ORDER BY coin_id,last_updated DESC
                       ON CONFLICT(coin_id)
                       DO UPDATE 
                       SET 
                       symbol = EXCLUDED.symbol,
                       name_ = EXCLUDED.name_,
                       current_prices = EXCLUDED.current_prices,
                       market_cap = EXCLUDED.market_cap,
                       market_cap_rank = EXCLUDED.market_cap_rank,
                       total_volume = EXCLUDED.total_volume,
                       price_change_percentage_24h = EXCLUDED.price_change_percentage_24h,
                       last_updated = EXCLUDED.last_updated,
                       refresh_time = CURRENT_TIMESTAMP;
                       """)
        connection.commit()
        logger.info("Data loaded to Gold overview successfully")
    except psycopg2.Error as e:
        logger.error(f"Database Error: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def insert_gold_market_statistics():
    connection, cursor = None,None
    try:
        connection,cursor = get_connection()
        if connection is None or cursor is None:
            logger.warning("Could not connect to database, aborting insert to Gold statistics")
            return
        cursor.execute("""INSERT INTO gold_market_statistics(
                       coin_id,
                       symbol,
                       name_,
                       average_price,
                       average_volume,
                       highest_price,
                       lowest_price,
                       average_market_cap,
                       price_volatility)
                       SELECT
                       coin_id,
                       symbol,
                       name_,
                       AVG(prices) AS average_price,
                       AVG(total_volume) AS average_volume,
                       MAX(prices) AS highest_price,
                       MIN(prices) AS lowest_price,
                       AVG(market_cap) AS average_market_cap,
                       STDDEV(prices) AS price_volatility
                       FROM dim_crypto_asset
                       JOIN fact_crypto_market ON  
                       dim_crypto_asset.id = fact_crypto_market.dim_id
                       GROUP BY
                       coin_id,
                       symbol,
                       name_
                       ON CONFLICT(coin_id)
                       DO UPDATE
                       SET 
                       symbol = EXCLUDED.symbol,
                       name_ = EXCLUDED.name_,
                       average_price = EXCLUDED.average_price,
                       average_volume = EXCLUDED.average_volume,
                       highest_price = EXCLUDED.highest_price,
                       lowest_price = EXCLUDED.lowest_price,
                       average_market_cap = EXCLUDED.average_market_cap,
                       price_volatility = EXCLUDED.price_volatility,
                       refresh_time = CURRENT_TIMESTAMP;
                       """)
        connection.commit()
        logger.info("Data loaded to gold statistics successfully")
    except psycopg2.Error as e:
        logger.error(f"Database Error: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
