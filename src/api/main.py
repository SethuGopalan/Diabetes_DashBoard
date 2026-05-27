# Import FastAPI framework for creating APIs
from fastapi import FastAPI 

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

    # Return JSON response back to browser/client
    return {"status": "API running"}


  
    
