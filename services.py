"""A script meant to contain all the services logic"""
from database import base, engine


def create_db():
    """The database creation method

    Returns:
        _type_: created the database
    """
    return base.metadata.create_all(bind=engine)
