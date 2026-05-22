from sqlalchemy import create_engine
from models import Base

DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/meeting_summarizer"

engine = create_engine(DATABASE_URL)


with engine.connect() as conn:
    print("Connected successfully!")
    
Base.metadata.create_all(bind=engine)
