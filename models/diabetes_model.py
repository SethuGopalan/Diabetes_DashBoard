from sqlalchemy import Column,Integer,Float,BigInteger
# Import ORM base creator
from sqlalchemy.orm import declarative_base

# Create ORM base class
Base = declarative_base()

class Diabetespatients(Base):

    __tablename__ ="diabetes_clean"

    # Map this ORM class to PostgreSQL table
    __tablename__ = "diabetes_clean"

    # Primary key for ORM

    id = Column(BigInteger, primary_key=True)

    # Integer SQL column
    pregnancies = Column(Integer)

    # Float SQL column
    glucose = Column(Float)

    # Float SQL column
    diastolic = Column(Float)

    # Float SQL column
    triceps = Column(Float)

    # Float SQL column
    insulin = Column(Float)

    # Float SQL column
    bmi = Column(Float)

    # Float SQL column
    dpf = Column(Float)

    # Integer SQL column
    age = Column(Integer)

    # Integer SQL column
    diabetes = Column(Integer)