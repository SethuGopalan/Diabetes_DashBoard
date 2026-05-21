# import Python logging module
import logging

# import JSON module for structured log messages
import json

# import os module for future environment/path handling
import os

# import SparkSession from PySpark
from pyspark.sql import SparkSession


# configure logger settings
# INFO = normal pipeline messages
# format = how logs appear in terminal
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s'
)


# custom logger function
def log_json(message, level="ERROR"):

    # create JSON formatted log message
    entry = json.dumps({
        "status": level,
        "msg": message
    })

    # if error log
    if level == "ERROR":

        # print error log
        logging.error(entry)

    # otherwise normal info log
    else:

        # print info log
        logging.info(entry)


# data loader function
def load_data(file_path):

    # log pipeline started
    log_json("log pipeline started", level="INFO")

    # create Spark session
    spark = SparkSession.builder \
        .appName("data_loader") \
        .config("spark.jars.packages", "org.postgresql:postgresql:42.7.3") \
        .getOrCreate()

    # load CSV file into Spark dataframe
    raw_data = spark.read.csv(
        file_path,
        header=True,
        inferSchema=True
    )

    # return Spark dataframe
    return raw_data