# ============================================================
# IMPORTS
# Purpose:
# Load environment settings and connect to
# the Terrafox Data Lake.
# ============================================================

import os
from dotenv import load_dotenv
import terrafox_datalake as dl

# ============================================================
# ENVIRONMENT CONFIGURATION
# Purpose:
# Load MinIO credentials and data location
# from the project's .env file.
# ============================================================

load_dotenv()


# ============================================================
# DATA LAKE READER
# Purpose:
# Read Diabetes.csv directly from the Terrafox
# Data Lake into a PySpark DataFrame.
# ============================================================


def load_csv_from_datalake(spark):

    # Get MinIO bucket from .env
    bucket = os.getenv("DATALAKE_BUCKET", "bigdata")

    # Get file location inside the bucket
    key = os.getenv("DATALAKE_KEY", "Data/Diabetes.csv")

    # ========================================================
    # CONNECT TO DATA LAKE
    # Purpose:
    # dl.connect() reads MINIO_USER,
    # MINIO_PASSWORD and MINIO_ENDPOINT
    # from the environment.
    # ========================================================

    dl.connect()
    # ============================================================
    # SPARK S3A CONFIGURATION
    # Purpose:
    # Configure Spark/Hadoop to access the Terrafox
    # MinIO S3-compatible Data Lake.
    # ============================================================

    hadoop_config = spark.sparkContext._jsc.hadoopConfiguration()

    # MinIO credentials
    hadoop_config.set("fs.s3a.access.key", os.getenv("MINIO_USER"))

    hadoop_config.set("fs.s3a.secret.key", os.getenv("MINIO_PASSWORD"))

    # Terrafox MinIO endpoint
    hadoop_config.set("fs.s3a.endpoint", os.getenv("MINIO_ENDPOINT"))

    # MinIO/S3-compatible storage should use path-style access
    hadoop_config.set("fs.s3a.path.style.access", "true")

    # Explicitly tell Hadoop to use access-key/secret-key credentials
    hadoop_config.set(
        "fs.s3a.aws.credentials.provider",
        "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider",
    )

    # Region used for S3 request signing
    hadoop_config.set("fs.s3a.endpoint.region", os.getenv("MINIO_REGION", "us-east-1"))

    # ========================================================
    # LOAD DATA INTO PYSPARK
    # Purpose:
    # Read the CSV directly from MinIO without
    # first downloading it into Data/raw.
    # ========================================================

    raw_data = dl.read_csv_spark(
        spark=spark, bucket=bucket, key=key, header=True, infer_schema=True
    )

    # Return Spark DataFrame to data_loader.py
    return raw_data
