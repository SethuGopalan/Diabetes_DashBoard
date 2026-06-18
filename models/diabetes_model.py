from sqlalchemy import Column, Integer, Float, BigInteger
from src.database.db_connection import Base


class DiabetesPatient(Base):
    """
    ORM model for diabetes_clean table.
    Each class variable maps to one database column.
    """

    __tablename__ = "diabetes_clean"

    id = Column(BigInteger, primary_key=True)

    pregnancies = Column(Integer)
    glucose = Column(Float)
    diastolic = Column(Float)
    triceps = Column(Float)
    insulin = Column(Float)
    bmi = Column(Float)
    dpf = Column(Float)
    age = Column(Integer)
    diabetes = Column(Integer)