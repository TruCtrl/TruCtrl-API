# SQLite database setup for TruCtrl-API using SQLModel
import os
from sqlmodel import SQLModel, create_engine, Session
from .config import config

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tructrl.db')
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(
    config.sqlalchemy_database_url, connect_args={"check_same_thread": False}
)

# Dependency for getting a session

def get_session():
    with Session(engine) as session:
        yield session

# For creating tables

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
