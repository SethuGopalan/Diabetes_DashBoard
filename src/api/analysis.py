from fastapi import APIRouter
from src.database.db_connection import get_db_connection 
from src.data_pipeline.data_loader import log_json


router = APIRouter()

@router.get("/analysis/{analysis_type}")

def analysis_endpoint(analysis_type):
    log_json("Analysis endpoind accessed...",level="INFO")
    conn = get_db_connection()
        
    # total columnsname
    curr = conn.cursor()
    try:
        if analysis_type == "age":
            curr.execute("SELECT CASE WHEN age <=29 THEN '20-29' WHEN age <=39 THEN '30-39' WHEN age <=49 THEN '40-49' WHEN age <=59 THEN '50-59'ELSE '60+'  END age_group, COUNT(*) AS total_patient,COUNT (CASE WHEN diabetes=1 THEN 1 ELSE NULL END ) AS diabetic_patients, ROUND(COUNT(CASE WHEN diabetes=1 THEN 1 ELSE NULL END )* 100.0 / COUNT(*),2)  AS diabetic_persentage FROM diabetes_clean GROUP BY 1 ")   
            rows = curr.fetchall()
            result=[{

                "age_group": row[0],
                "total_patients": row[1],
                "diabetic_patients":row[2],
                "diabetes_percentage":float(row[3])
            }
            for row in rows
            ]
            return {
                    "analysis_type":"age",
                    "data":result
                }
    

        # {"message":"age endpoint"}
        elif analysis_type == "bmi":
            return {"message":"bmi endpoint"}
        elif analysis_type == "glucose":
            return {"message":"glucose endpoint"}
        elif analysis_type == "pregnancy":
            return {"message":"pregnancy endpoint"}
        if analysis_type == "combined":
            return {"message":"combined endpoint"}
    finally:
        curr.close()
        conn.close()
    
