"""A script meant to contain all the services logic"""
from database import base, engine, session_local
import models


def create_db():
    """The database creation method

    Returns:
        _type_: created the database 
    """
    return base.metadata.create_all(bind=engine)


def get_db():
    """A function to create a database session

    Yields:
        Database: The database session
    """
    _db = session_local()

    try:
        yield _db
    finally:
        _db.close()
