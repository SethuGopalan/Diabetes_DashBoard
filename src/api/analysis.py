# ============================================================
# PART 1: IMPORT REQUIRED MODULES
# Purpose:
# - APIRouter creates analysis API routes.
# - Database connection provides access to PostgreSQL.
# - log_json records API activity in the application logs.
# ============================================================

from fastapi import APIRouter
from src.database.db_connection import get_db_connection
from src.data_pipeline.data_loader import log_json

# ============================================================
# PART 2: CREATE ANALYSIS ROUTER
# Purpose:
# - Creates a separate FastAPI router for analysis endpoints.
# - This router will later be registered inside main.py.
# ============================================================

router = APIRouter()


# ============================================================
# PART 3: CREATE DYNAMIC ANALYSIS ENDPOINT
# Purpose:
# - Accepts the analysis type from the URL.
#
# Examples:
# /analysis/age
# /analysis/bmi
# /analysis/glucose
# /analysis/pregnancy
# /analysis/combined
# ============================================================


@router.get("/analysis/{analysis_type}")
def analysis_endpoint(analysis_type: str):

    # --------------------------------------------------------
    # PART 4: LOG API REQUEST
    # Purpose:
    # - Records whenever the analysis endpoint is accessed.
    # --------------------------------------------------------

    log_json(f"Analysis endpoint accessed: {analysis_type}", level="INFO")

    # --------------------------------------------------------
    # PART 5: CONNECT TO POSTGRESQL
    # Purpose:
    # - Opens the database connection.
    # - Creates a cursor for executing SQL queries.
    # --------------------------------------------------------

    conn = get_db_connection()
    curr = conn.cursor()

    try:

        # ====================================================
        # PART 6: AGE ANALYSIS
        # Purpose:
        # - Groups patients into age ranges.
        # - Counts total patients in each age group.
        # - Counts diabetic patients.
        # - Calculates diabetes percentage.
        # ====================================================

        if analysis_type == "age":

            curr.execute("""
                    SELECT
                        CASE
                            WHEN age <= 29 THEN '20-29'
                            WHEN age <= 39 THEN '30-39'
                            WHEN age <= 49 THEN '40-49'
                            WHEN age <= 59 THEN '50-59'
                            ELSE '60+'
                        END AS age_group,

                        COUNT(*) AS total_patients,

                        COUNT(
                            CASE
                                WHEN diabetes = 1 THEN 1
                                ELSE NULL
                            END
                        ) AS diabetic_patients,

                        ROUND(
                            COUNT(
                                CASE
                                    WHEN diabetes = 1 THEN 1
                                    ELSE NULL
                                END
                            ) * 100.0 / COUNT(*),
                            2
                        ) AS diabetes_percentage

                    FROM diabetes_clean

                    GROUP BY 1

                    ORDER BY MIN(age);
                    """)

            # ------------------------------------------------
            # PART 7: FETCH AGE ANALYSIS RESULTS
            # Purpose:
            # - Retrieves all rows returned by PostgreSQL.
            # ------------------------------------------------

            rows = curr.fetchall()

            # ------------------------------------------------
            # PART 8: CONVERT AGE RESULTS TO JSON FORMAT
            # Purpose:
            # - Converts PostgreSQL tuples into dictionaries.
            # - FastAPI can return these directly as JSON.
            # ------------------------------------------------

            result = [
                {
                    "age_group": row[0],
                    "total_patients": row[1],
                    "diabetic_patients": row[2],
                    "diabetes_percentage": float(row[3]),
                }
                for row in rows
            ]

            # ------------------------------------------------
            # PART 9: RETURN AGE ANALYSIS RESPONSE
            # Purpose:
            # - Sends age analysis results to the frontend.
            # ------------------------------------------------

            return {"analysis_type": "age", "data": result}

        # ====================================================
        # PART 10: BMI ANALYSIS
        # Purpose:
        # - Groups patients by BMI category.
        # - Counts total patients in each BMI group.
        # - Counts diabetic patients.
        # - Calculates diabetes percentage.
        # ====================================================

        elif analysis_type == "bmi":

            curr.execute("""
                    SELECT
                        CASE
                            WHEN bmi < 18.5 THEN 'Underweight'
                            WHEN bmi < 25.0 THEN 'Healthy Weight'
                            WHEN bmi < 30.0 THEN 'Overweight'
                            WHEN bmi < 35.0 THEN 'Obesity Class 1'
                            WHEN bmi < 40.0 THEN 'Obesity Class 2'
                            ELSE 'Obesity Class 3'
                        END AS bmi_group,

                        COUNT(*) AS total_patients,

                        COUNT(
                            CASE
                                WHEN diabetes = 1 THEN 1
                                ELSE NULL
                            END
                        ) AS diabetic_patients,

                        ROUND(
                            COUNT(
                                CASE
                                    WHEN diabetes = 1 THEN 1
                                    ELSE NULL
                                END
                            ) * 100.0 / COUNT(*),
                            2
                        ) AS diabetes_percentage

                    FROM diabetes_clean

                    GROUP BY 1;
                    """)

            # ------------------------------------------------
            # PART 11: FETCH BMI ANALYSIS RESULTS
            # Purpose:
            # - Retrieves all rows returned by PostgreSQL.
            # ------------------------------------------------

            rows = curr.fetchall()

            # ------------------------------------------------
            # PART 12: CONVERT BMI RESULTS TO JSON FORMAT
            # Purpose:
            # - Converts PostgreSQL tuples into dictionaries.
            # - FastAPI can return these directly as JSON.
            # ------------------------------------------------

            result = [
                {
                    "bmi_group": row[0],
                    "total_patients": row[1],
                    "diabetic_patients": row[2],
                    "diabetes_percentage": float(row[3]),
                }
                for row in rows
            ]

            # ------------------------------------------------
            # PART 13: RETURN BMI ANALYSIS RESPONSE
            # Purpose:
            # - Sends BMI analysis results to the frontend.
            # ------------------------------------------------

            return {"analysis_type": "bmi", "data": result}

        # ====================================================
        # PART 14: GLUCOSE ANALYSIS
        # Purpose:
        # - Groups patients by glucose category.
        # - Counts total patients in each glucose group.
        # - Counts diabetic patients.
        # - Calculates diabetes percentage.
        # ====================================================

        elif analysis_type == "glucose":

            curr.execute("""
                    SELECT
                        CASE
                            WHEN glucose < 140 THEN 'Normal'
                            WHEN glucose < 200 THEN 'Prediabetes'
                            ELSE 'Diabetes'
                        END AS glucose_group,

                        COUNT(*) AS total_patients,

                        COUNT(
                            CASE
                                WHEN diabetes = 1 THEN 1
                                ELSE NULL
                            END
                        ) AS diabetic_patients,

                        ROUND(
                            COUNT(
                                CASE
                                    WHEN diabetes = 1 THEN 1
                                    ELSE NULL
                                END
                            ) * 100.0 / COUNT(*),
                            2
                        ) AS diabetes_percentage

                    FROM diabetes_clean

                    GROUP BY 1;
                    """)

            # ------------------------------------------------
            # PART 15: FETCH GLUCOSE ANALYSIS RESULTS
            # Purpose:
            # - Retrieves all rows returned by PostgreSQL.
            # ------------------------------------------------

            rows = curr.fetchall()

            # ------------------------------------------------
            # PART 16: CONVERT GLUCOSE RESULTS TO JSON FORMAT
            # Purpose:
            # - Converts PostgreSQL tuples into dictionaries.
            # - FastAPI can return these directly as JSON.
            # ------------------------------------------------

            result = [
                {
                    "glucose_group": row[0],
                    "total_patients": row[1],
                    "diabetic_patients": row[2],
                    "diabetes_percentage": float(row[3]),
                }
                for row in rows
            ]

            # ------------------------------------------------
            # PART 17: RETURN GLUCOSE ANALYSIS RESPONSE
            # Purpose:
            # - Sends glucose analysis results to the frontend.
            # ------------------------------------------------

            return {"analysis_type": "glucose", "data": result}

        # ====================================================
        # PART 18: PREGNANCY ANALYSIS
        # Purpose:
        # - Groups patients by number of pregnancies.
        # - Counts total patients in each group.
        # - Counts diabetic patients in each group.
        # - Calculates diabetes percentage.
        # ====================================================

        elif analysis_type == "pregnancy":

            curr.execute("""
                    SELECT
                        CASE
                            WHEN pregnancies <= 2 THEN '0-2'
                            WHEN pregnancies <= 5 THEN '3-5'
                            WHEN pregnancies <= 9 THEN '6-9'
                            ELSE '10+'
                        END AS pregnancies_group,

                        COUNT(*) AS total_patients,

                        COUNT(
                            CASE
                                WHEN diabetes = 1 THEN 1
                                ELSE NULL
                            END
                        ) AS diabetic_patients,

                        ROUND(
                            COUNT(
                                CASE
                                    WHEN diabetes = 1 THEN 1
                                    ELSE NULL
                                END
                            ) * 100.0 / COUNT(*),
                            2
                        ) AS diabetes_percentage

                    FROM diabetes_clean

                    GROUP BY 1;
                    """)

            # ------------------------------------------------
            # PART 19: FETCH PREGNANCY ANALYSIS RESULTS
            # Purpose:
            # - Retrieves all rows returned by PostgreSQL.
            # ------------------------------------------------

            rows = curr.fetchall()

            # ------------------------------------------------
            # PART 20: CONVERT PREGNANCY RESULTS TO JSON FORMAT
            # Purpose:
            # - Converts PostgreSQL tuples into dictionaries.
            # - FastAPI can return these directly as JSON.
            # ------------------------------------------------

            result = [
                {
                    "pregnancies_group": row[0],
                    "total_patients": row[1],
                    "diabetic_patients": row[2],
                    "diabetes_percentage": float(row[3]),
                }
                for row in rows
            ]

            # ------------------------------------------------
            # PART 21: RETURN PREGNANCY ANALYSIS RESPONSE
            # Purpose:
            # - Sends pregnancy analysis results to the frontend.
            # ------------------------------------------------

            return {"analysis_type": "pregnancy", "data": result}

            # ====================================================
            # PART 22: COMBINED RISK ANALYSIS
            # Purpose:
            # - Placeholder for combined risk-factor analysis.
            # ====================================================

        elif analysis_type == "combined":
            curr.execute("""
                    SELECT
                        risk_count,

                        COUNT(*) AS total_patients,

                        COUNT(
                            CASE
                                WHEN diabetes = 1 THEN 1
                                ELSE NULL
                            END
                        ) AS diabetic_patients,

                        ROUND(
                            COUNT(
                                CASE
                                    WHEN diabetes = 1 THEN 1
                                    ELSE NULL
                                END
                            ) * 100.0 / COUNT(*),
                            2
                        ) AS diabetes_percentage

                    FROM (
                        SELECT
                            diabetes,

                            (
                                CASE WHEN age >= 40 THEN 1 ELSE 0 END
                                +
                                CASE WHEN bmi >= 30 THEN 1 ELSE 0 END
                                +
                                CASE WHEN glucose >= 140 THEN 1 ELSE 0 END
                            ) AS risk_count

                        FROM diabetes_clean
                    ) AS combined_risk

                    GROUP BY risk_count

                    ORDER BY risk_count;
            
            
             """)

            # ------------------------------------------------
            # PART 19: FETCH PREGNANCY ANALYSIS RESULTS
            # Purpose:
            # - Retrieves all rows returned by PostgreSQL.
            # ------------------------------------------------

            rows = curr.fetchall()

            # ------------------------------------------------
            # PART 20: CONVERT PREGNANCY RESULTS TO JSON FORMAT
            # Purpose:
            # - Converts PostgreSQL tuples into dictionaries.
            # - FastAPI can return these directly as JSON.
            # ------------------------------------------------

            result = [
                {
                    "risk_count": row[0],
                    "total_patients": row[1],
                    "diabetic_patients": row[2],
                    "diabetes_percentage": float(row[3]),
                }
                for row in rows
            ]

            # ------------------------------------------------
            # PART 21: RETURN PREGNANCY ANALYSIS RESPONSE
            # Purpose:
            # - Sends pregnancy analysis results to the frontend.
            # ------------------------------------------------

            return {"analysis_type": "combined", "data": result}
        # ====================================================
        # PART 23: INVALID ANALYSIS TYPE
        # Purpose:
        # - Handles analysis names that do not exist.
        # ====================================================

        else:

            return {"message": f"Unknown analysis type: {analysis_type}"}

    # ========================================================
    # PART 24: CLOSE DATABASE CONNECTION
    # Purpose:
    # - Always closes the PostgreSQL cursor and connection.
    # - Runs even if an error happens during the query.
    # ========================================================

    finally:

        curr.close()
        conn.close()
