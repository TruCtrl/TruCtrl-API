# File:     database.py
# Package:  tructrl_api
# Project:  TruCtrl

# SQLite database setup for TruCtrl-API using SQLModel
import os
from sqlmodel import SQLModel, create_engine, Session
from .config import config
from dotenv import load_dotenv

load_dotenv()

# Use the environment variables for the database URL
DB_TYPE = os.getenv("DB_TYPE", "sqlite")
DB_NAME = os.getenv("DB_NAME", "tructrl.db")
DB_USER = os.getenv("DB_USER", "")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "")
DB_PORT = os.getenv("DB_PORT", "")

if DB_TYPE == "sqlite":
    SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_NAME}"
else:
    SQLALCHEMY_DATABASE_URL = f"{DB_TYPE}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False} if DB_TYPE == "sqlite" else {}
)

# Dependency for getting a session

def get_session():
    with Session(engine) as session:
        yield session

# For creating tables

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Add this to run table creation when the script is executed directly
if __name__ == "__main__":
    create_db_and_tables()
