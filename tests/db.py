import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base

engine = create_engine("sqlite:///./test.db", connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
