# ============================================================
# IMPORTS
# Purpose:
# Import logging, FastAPI routing, database connection,
# and PostgreSQL tools required by the /info endpoint.
# ============================================================

# Custom logging function used to record API activity
from src.data_pipeline.data_loader import log_json

# FastAPI router used to create API endpoints
from fastapi import APIRouter

# Custom PostgreSQL connection function
from src.database.db_connection import get_db_connection

# PostgreSQL Python driver
import psycopg2
import pandas as pd
# ============================================================
# API ROUTER
# Purpose:
# Create a FastAPI router that can later be included
# inside the main FastAPI application.
# ============================================================

router = APIRouter()


# ============================================================
# INFO ENDPOINT
# Purpose:
# Return general information about the diabetes_clean table.
#
# The endpoint returns:
# - Total rows
# - Total columns
# - Column names
# - Column data types
# - Head rows
# - Tail rows
# ============================================================


@router.get("/info")
def info_endpoint():

    # ========================================================
    # LOG API ACCESS
    # Purpose:
    # Record whenever the /info endpoint is called.
    # ========================================================

    log_json("Info endpoint accessed ...", level="INFO")

    # ========================================================
    # DATABASE CONNECTION
    # Purpose:
    # Open a connection to PostgreSQL.
    # ========================================================

    conn = get_db_connection()

    # ========================================================
    # DATABASE CURSOR
    # Purpose:
    # Create a cursor used to execute SQL queries.
    # ========================================================

    curr = conn.cursor()

    # ========================================================
    # DATABASE OPERATIONS
    # Purpose:
    # Run all SQL queries required by the /info endpoint.
    #
    # try/finally ensures the cursor and connection are
    # closed even if an error occurs.
    # ========================================================

    try:
        # ============================================================
        # DIABETIC PATIENT COUNT
        # Purpose:
        # Count the total number of patients where diabetes = 1.
        # This value is used in the Key Statistics section.
        # ============================================================
        curr.execute(
                """
                SELECT
                    COUNT(CASE WHEN diabetes = 1 THEN 1 END)
                FROM diabetes_clean;
                """
            )

        diabetic_patients = curr.fetchone()[0]
        # ============================================================
        # NON-DIABETIC PATIENT COUNT
        # Purpose:
        # Count the total number of patients where diabetes = 0.
        # This value is used in the Key Statistics section.
        # ============================================================
        
        curr.execute(
                """
                SELECT
                    COUNT(CASE WHEN diabetes = 0 THEN 1 END)
                FROM diabetes_clean;
                """
            )

        non_diabetic_patients = curr.fetchone()[0]
        # ============================================================
        # DIABETES PREVALENCE
        # Purpose:
        # Calculate the percentage of patients in the dataset
        # who are classified as diabetic.
        # This value is used in the Key Statistics section.
        # ============================================================
        curr.execute(
            """
            SELECT
                ROUND(
                    COUNT(CASE WHEN diabetes = 1 THEN 1 END) * 100.0 / COUNT(*),
                    2
                )
            FROM diabetes_clean;
            """
        )
        diabetes_prevalence = curr.fetchone()[0]
        # ====================================================
        # COLUMN NAMES
        # Purpose:
        # Get all column names from diabetes_clean.
        # ====================================================

        curr.execute("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = 'diabetes_clean';
            """)

        column_name = curr.fetchall()

        # ====================================================
        # COLUMN DATA TYPES
        # Purpose:
        # Get the PostgreSQL data type for every column
        # inside diabetes_clean.
        # ====================================================

        curr.execute("""
            SELECT column_name, data_type
            FROM information_schema.columns
            WHERE table_name = 'diabetes_clean';
            """)

        data_type = curr.fetchall()

        # ====================================================
        # TOTAL ROW COUNT
        # Purpose:
        # Count the total number of patient records
        # stored inside diabetes_clean.
        # ====================================================

        curr.execute("""
            SELECT COUNT(*)
            FROM diabetes_clean;
            """)

        total_rows = curr.fetchone()[0]

        # ====================================================
        # TOTAL COLUMN COUNT
        # Purpose:
        # Count how many columns exist in diabetes_clean.
        # ====================================================

        curr.execute("""
            SELECT COUNT(*)
            FROM information_schema.columns
            WHERE table_name = 'diabetes_clean';
            """)

        total_columns = curr.fetchone()[0]

        # ====================================================
        # HEAD DATA
        # Purpose:
        # Retrieve records that will be used by the
        # dashboard Head table.
        # ====================================================

        curr.execute("""
            SELECT *
            FROM diabetes_clean
            ORDER BY id DESC;

            """)

        head_rows = curr.fetchall()

        # ====================================================
        # TAIL DATA
        # Purpose:
        # Retrieve records that will be used by the
        # dashboard Tail table.
        # ====================================================

        curr.execute("""
            SELECT *
            FROM diabetes_clean
            ORDER BY id ASC

            """)

        tail_rows = curr.fetchall()

        # ====================================================
        # API RESPONSE
        # Purpose:
        # Convert database query results into a dictionary
        # that FastAPI will return as JSON to the Dash app.
        # ====================================================
        # ============================================================
        # CORRELATION MATRIX
        # Purpose:
        # Retrieve numeric patient features and calculate correlations
        # between all features for the dashboard correlation heatmap.
        # The id column is excluded because it is only an identifier.
        # ============================================================

        curr.execute(
            """
            SELECT
                pregnancies,
                glucose,
                diastolic,
                                
                bmi,
                dpf,
                age,
                diabetes
            FROM diabetes_clean;
            """
        )

        correlation_rows = curr.fetchall()

        correlation_columns = [
            "pregnancies",
            "glucose",
            "diastolic",
                        
            "bmi",
            "dpf",
            "age",
            "diabetes",
        ]
        correlation_df = pd.DataFrame(
        correlation_rows,
        columns=correlation_columns,
        )
        correlation_rows = curr.fetchall()

        # correlation_df = pd.DataFrame(
        #  correlation_rows,
        # columns=correlation_columns,
        # )
        correlation_df = correlation_df.apply(pd.to_numeric, errors="coerce")
        correlation_matrix = correlation_df.corr().round(2)
        correlation_matrix = correlation_matrix.fillna(0)
        return {
            "correlation_columns": correlation_matrix.columns.tolist(),
            "correlation_matrix": correlation_matrix.values.tolist(),
            "diabetic_patients":diabetic_patients, 
            "non_diabetic_patients":non_diabetic_patients,
            "diabetes_prevalence":diabetes_prevalence,
            "total_rows": total_rows,
            "total_columns": total_columns,
            "column_names": [col[0] for col in column_name],
            "data_types": {col[0]: col[1] for col in data_type},
            "head_rows": head_rows,
            "tail_rows": tail_rows,
        }

    # ========================================================
    # DATABASE CLEANUP
    # Purpose:
    # Always close the database cursor and connection,
    # whether the API succeeds or an error occurs.
    # ========================================================

    finally:

        curr.close()

        conn.close()
