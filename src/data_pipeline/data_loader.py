# ============================================================
# IMPORTS
# Purpose:
# Import logging, JSON tools, PySpark,
# and the Terrafox Data Lake reader.
# ============================================================

import logging
import json

from pyspark.sql import SparkSession

from src.data_pipeline.datalake_reader import load_csv_from_datalake


# ============================================================
# LOGGING CONFIGURATION
# Purpose:
# Configure normal pipeline logging.
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s"
)


# ============================================================
# JSON LOGGER
# Purpose:
# Create structured JSON log messages.
# ============================================================

def log_json(message, level="ERROR"):

    entry = json.dumps({
        "status": level,
        "msg": message
    })

    if level == "ERROR":
        logging.error(entry)

    else:
        logging.info(entry)


# ============================================================
# DATA LOADER
# Purpose:
# Create the Spark session and load raw data
# from the Terrafox Data Lake into PySpark.
# ============================================================

def load_data():

    # Log pipeline start
    log_json(
        "Data loading pipeline started",
        level="INFO"
    )


    # ========================================================
    # CREATE SPARK SESSION
    # Purpose:
    # Create the PySpark environment used by
    # the data cleaning pipeline.
    # ========================================================

    spark = (
        SparkSession.builder
        .appName("data_loader")
        .config(
            "spark.jars.packages",
            "org.postgresql:postgresql:42.7.3,"
            "org.apache.hadoop:hadoop-aws:3.4.2"
        )
        .getOrCreate()
    )


    # ========================================================
    # LOAD RAW DATA FROM DATA LAKE
    # Purpose:
    # datalake_reader.py connects to MinIO and
    # returns Diabetes.csv as a Spark DataFrame.
    # ========================================================

    raw_data = load_csv_from_datalake(spark)


    # Return Spark DataFrame to data_cleaner.py
    return raw_data