import pandas as pd
from database import extract_bronze_data
from logger import logger

def read_bronze_data():
    data = extract_bronze_data()
    df = pd.DataFrame(data)
    logger.info("Bronze data loaded into DataFrame")
    return df


def fix_types(df):
    columns = ["current_price", "market_cap", "total_volume",
                "high_24h", "low_24h","price_change_24h",
                "price_change_percentage_24h"]
    df[columns] = df[columns].astype(float)
    logger.info("Data types fixed successfully")
    return df

def fix_duplicates(df):
    df = df.drop_duplicates(subset=["coin_id","ingestion_time"])
    logger.info("Duplicates dropped successfully")
    return df

def validate_ranges(df):
    columns = df[["current_price","market_cap",
                "market_cap_rank","total_volume"
                ,"high_24h","low_24h"]]
    filt = (columns > 0).all(axis=1)
    df = df[filt]
    logger.info("Data validated successfully")
    return df

def transform_silver():
    df = read_bronze_data()
    df = fix_types(df)
    df = fix_duplicates(df)
    data = validate_ranges(df)
    logger.info("Data sucessfully transformed to Silver")
    return data