"""
This script cleans the diabetes dataset using PySpark and Pandas.
PySpark is used for large-scale dataframe processing and pipeline operations.
Pandas is used only for easier median calculation during zero-value replacement.
Cleaning steps include duplicate removal, null value checking, and invalid zero replacement.
Invalid medical zeros are replaced with median values for better data quality.
"""

# Import SparkSession for Spark application creation
from pyspark.sql import SparkSession

# Import when function for conditional column updates
from pyspark.sql.functions import when

# Import custom data loading function
from data_loader import load_data

# Import pandas for median calculations
import pandas as pd

def clean_data():


    # =========================================================
    # LOAD RAW DATA
    # =========================================================

    # Load diabetes CSV dataset
    raw_data = load_data("Data/raw/Diabetes.csv")


    # =========================================================
    # REMOVE DUPLICATES
    # =========================================================

    # Count rows before duplicate removal
    before_count = raw_data.count()

    # Remove duplicate rows
    clean_df = raw_data.dropDuplicates()

    # Count rows after duplicate removal
    after_count = clean_df.count()

    # Calculate removed duplicate rows
    duplicate_removed = before_count - after_count

    # Print duplicate cleaning results
    # print("Before:", before_count)
    # print("After:", after_count)
    # print("Duplicates Removed:", duplicate_removed)


    # =========================================================
    # CHECK NULL VALUES
    # =========================================================

    # Get all dataframe column names
    clean_df_col = clean_df.columns

    # Loop through each column
    for col in clean_df_col:

        # Count null values in current column
        null_count = clean_df.filter(
            clean_df[col].isNull()
        ).count()

        # Print column name and null count
        # print(col, null_count)

        # Print separator
        # print("__________________________")


    # Print section separator
    # print("********************************************************")


    # =========================================================
    # CHECK INVALID ZERO VALUES
    # =========================================================

    # Medical columns where zero is invalid
    invalid_zeros = [
        "glucose",
        "diastolic",
        "triceps",
        "insulin",
        "bmi"
    ]


    # Convert selected Spark columns to Pandas dataframe
    # Used only for easy median calculation
    pandas_df = clean_df.select(
        invalid_zeros
    ).toPandas()


    # Loop through each invalid zero column
    for invalid in invalid_zeros:

        # Count zero values before cleaning
        zeros_incol = clean_df.filter(
            clean_df[invalid] == 0
        ).count()

        # Print zero count before cleaning
        # print(invalid, zeros_incol)

        # Calculate median excluding zero values
        median_value = pandas_df[
            pandas_df[invalid] != 0
        ][invalid].median()

        # Replace zero values with median value
        clean_df = clean_df.withColumn(
            invalid,
            when(
                clean_df[invalid] == 0,
                median_value
            ).otherwise(
                clean_df[invalid]
            )
        )

        # Count zero values after cleaning
        zeros_incol = clean_df.filter(
            clean_df[invalid] == 0
        ).count()

        # Print remaining zero count after cleaning
        # print(f"after clean {invalid}: {zeros_incol}")


    # =========================================================
    # FINAL CLEAN DATA OUTPUT
    # =========================================================

    # Show cleaned dataframe
    
    # clean_df.show()
        
    return clean_df 