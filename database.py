"""The database configuration file"""
import sqlalchemy
import sqlalchemy.ext.declarative
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


DB_URL = "sqlite:///.dbfile.db"

engine = create_engine(DB_URL, connect_args={"check_same_thread"})

session_local = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)
