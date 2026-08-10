# Import FastAPI framework for creating APIs
from fastapi import FastAPI 
from src.data_pipeline.data_loader import log_json

# Import uvicorn server for running the FastAPI application
import uvicorn
from src.database.db_connection import get_db
from src.database.db_connection import SessionLocal
from models.diabetes_model import DiabetesPatient
from src.api.info import router as info_router
from src.api.analysis import router as analysis_router
# Create FastAPI application object
app = FastAPI()
app.include_router(info_router)
app.include_router(analysis_router)
# Create GET endpoint for root URL "/"
# When user visits localhost:8000/
# this function will run
@app.get("/")

# Function that handles requests for "/"
def root_endpoint():

    log_json("Root endpoint accesses ...",level="INFO")
    # Return JSON response back to browser/client
    return {"status": "API running"}
@app.get("/summary")

def summary_status():

    db = SessionLocal()

    total_patients=db.query(DiabetesPatient).count()
      
    db.close()
    return {"total_patients":total_patients}
   
    



  
    
