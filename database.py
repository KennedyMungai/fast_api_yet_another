"""The database configuration file"""
import sqlalchemy
import sqlalchemy.ext.declarative
import sqlalchemy.orm
from sqlalchemy import create_engine


DB_URL = "sqlite:///.dbfile.db"

engine = create_engine(DB_URL, connect_args={"check_same_thread"})
