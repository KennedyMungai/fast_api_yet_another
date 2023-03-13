"""A script meant to contain all the services logic"""
from database import base, engine, session_local
from models import UserModel
from sqlalchemy import orm


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


async def get_user_by_email(_email: str, _db: orm.Session) -> bool:
    """Gets user by mail

    Args:
        _email (str): The email address of the user
        _db (orm.Session): The database session

    Returns:
        bool: Returns a bool of whether the email is in the database or not
    """
    return _db.query(UserModel).filter(UserModel.email == _email).first()
