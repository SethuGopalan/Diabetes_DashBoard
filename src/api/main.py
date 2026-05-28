# Import FastAPI framework for creating APIs
from fastapi import FastAPI 
from src.data_pipeline.data_loader import log_json

# Import uvicorn server for running the FastAPI application
import uvicorn

# Create FastAPI application object
app = FastAPI()

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
    log_json("Summery acees started ...",level="INFO")
     # Load connection credentials from the local .env configuration file
    load_dotenv()
    # Connect to PostgreSQL
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")



  
    
