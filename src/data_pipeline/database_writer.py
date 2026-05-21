from data_cleaner import clean_data
from data_loader import log_json
import psycopg2
from dotenv import load_dotenv
import os
def write_to_database():
    """
    Fetches cleaned data from the pipeline and loads it into a PostgreSQL database.

    This function coordinates the final step of the ETL (Extract, Transform, Load) 
    pipeline. It loads database credentials from an environment configuration, 
    triggers the data-cleaning process to get a PySpark DataFrame, establishes a 
    native JDBC connection to PostgreSQL, and safely writes the schema and data 
    using an 'overwrite' mode. The execution is fully wrapped in structured JSON logging.
    """

    # Load connection credentials from the local .env configuration file
    load_dotenv()
    # Connect to PostgreSQL
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    # Send pipeline kickoff notice to the central logger
    log_json("Fetching cleaned data from pipeline...", level="INFO")

    try:
        # Step 1: Call data_cleaner.py to run the loading/cleaning pipeline 
        # and retrieve the final PySpark DataFrame

        #  Get clean data
        clean_df = clean_data()

        # Step 2: Build the structural PostgreSQL JDBC connection string
        jdbc_url = f"jdbc:postgresql://{db_host}:{db_port}/{db_name}"

        # Step 3: Define Spark JDBC properties including the Java database driver class
        connection_properties = {
        "user": db_user,
        "password": db_password,
        "driver": "org.postgresql.Driver"  # Tells Spark how to communicate with Postgres
        }
        log_json("Writing data to PostgreSQL table 'diabetes_clean'...", level="INFO")

        # Step 4: Stream the distributed Spark DataFrame directly into PostgreSQL.
        # Spark natively maps Python types to SQL types and handles table creation.

        clean_df.write.jdbc(
            url=jdbc_url,
            table="diabetes_clean",
            mode="overwrite",
            properties=connection_properties
        )
        # Confirm successful pipeline completion
        log_json("Table 'diabetes_clean' successfully created and populated!", level="INFO")
                
    except Exception as e:
        # Catch any structural or network failures and route them to the error logs
        log_json(f"Database write failed: {str(e)}", level="ERROR")
# Safeguard block: ensures this script only runs when executed directly,
# preventing it from executing unexpectedly if imported by other scripts.
if __name__ == "__main__":
    write_to_database()