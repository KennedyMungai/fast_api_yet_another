"""The database configuration file"""
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine


DB_URL = "sqlite:///.dbfile.db"

engine = create_engine(DB_URL)

session_local = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)

base = declarative_base()
