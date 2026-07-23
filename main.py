from api import get_crypto_data
from transform import transform_silver
from database import insert_bronze_data,insert_silver_data,insert_gold_market_overview,insert_gold_market_statistics,get_connection
from logger import logger
import traceback
import psycopg2

def run_pipeline():

    connection, cursor = None, None
    try:
        logger.info("Pipeline started")
        print("pipeline started")

      
        data = get_crypto_data()

       
        insert_bronze_data(data)

       
        data = transform_silver()
        
        
        connection, cursor = get_connection()

      
        insert_silver_data(data,cursor)
        
       
        insert_gold_market_overview(cursor)
        insert_gold_market_statistics(cursor)

        connection.commit()

        logger.info("Pipeline completed successfully")
        print("Pipeline completed successfully")

    except psycopg2.Error as e:
        print(f"Fail:",e)
        logger.error(f"Database error: {e}")
        if connection:
            connection.rollback()

    except Exception as e: 
        logger.error(f"Pipeline Error: {e}")
        print(" Pipeline Error:", e)
        traceback.print_exc()

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


if __name__ == "__main__":
    run_pipeline()