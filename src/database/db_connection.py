# Import dotenv loader to read values from .env file
from dotenv import load_dotenv

# Import SQLAlchemy engine creator
from sqlalchemy import create_engine

# Import os module for reading environment variables
import os
# Import sessionmaker utility for creating database sessions
from sqlalchemy.orm import sessionmaker 
# Load all variables from .env into memory
from sqlalchemy.orm import declarative_base

load_dotenv()

# Read PostgreSQL connection values from .env file
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")

# Build SQLAlchemy PostgreSQL connection URL
# Format:
# postgresql://username:password@host:port/database
database_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

# Create SQLAlchemy engine object
# Engine manages communication between Python and PostgreSQL
engine = create_engine(
    database_url
)
Base = declarative_base()
# Create session factory connected to the SQLAlchemy engine
# Every API request can create its own database session from this
SessionLocal=sessionmaker(
    # Bind all sessions to the PostgreSQL engine
    bind=engine
)



def get_db():

        
    db = SessionLocal()

    try:
        yield db

    finally:

        db.close()

        


