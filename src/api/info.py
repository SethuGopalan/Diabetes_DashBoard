
from src.data_pipeline.data_loader import log_json
from fastapi import APIRouter
from src.database.db_connection import get_db_connection 
import psycopg2

router = APIRouter()

# Create FastAPI application object
# app = FastAPI()

@router.get("/info")

def info_endpoint():
    
    log_json("Info endpoint accessed ...",level="INFO")

    conn = get_db_connection()
        
    # total columnsname
    curr = conn.cursor()
    try:

        curr.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'diabetes_clean';")

        column_name = curr.fetchall()
        # data type
        curr.execute("SELECT column_name,data_type FROM information_schema.columns WHERE table_name = 'diabetes_clean';")

        data_type = curr.fetchall()
        # total rows

        curr.execute("SELECT COUNT(*) FROM diabetes_clean;")

        total_rows = curr.fetchone()[0]


        curr.execute("SELECT COUNT(*) FROM information_schema.columns WHERE table_name = 'diabetes_clean';")
        total_columns = curr.fetchone()[0]

        # head
        curr.execute("SELECT * FROM diabetes_clean ")
        head_rows = curr.fetchall()

        # tail
        curr.execute("SELECT * FROM diabetes_clean  ")
        tail_rows = curr.fetchall()

            

        return {
                "total_rows": total_rows,
                "total_columns": total_columns,
                "column_names": [col[0] for col in column_name],
                "data_types": {col[0]: col[1] for col in data_type},
                "head_rows": head_rows,
                "tail_rows": tail_rows
            }  


    finally:
        curr.close()
        conn.close() 



