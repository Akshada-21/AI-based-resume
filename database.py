from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pandas as pd

Base = declarative_base()

class Result(Base):
    __tablename__ = 'results'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    score = Column(Float)
    email = Column(String)
    resume_path = Column(String)

engine = create_engine('sqlite:///resume.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

def store_result(name, score, email, resume_path):
    result = Result(name=name, score=score, email=email, resume_path=resume_path)
    session.add(result)
    session.commit()

def get_all_results():
    with engine.connect() as conn:
        df = pd.read_sql("SELECT * FROM results", conn)
    return df
