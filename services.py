"""A script meant to contain all the services logic"""
from database import base, engine, session_local
from models import UserModel
from sqlalchemy import orm
from schemas import UserRequest
from email_validator import validate_email, EmailNotValidError
from fastapi import HTTPException, status
from passlib import hash


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


async def create_user(_user: UserRequest, _db=orm.Session):
    """Created a user in the database

    Args:
        _user (UserRequest): The template of the user data coming in
        _db (_type_, optional): The database session. Defaults to orm.Session.

    Raises:
        HTTPException: Raises a bad request error whenever an email is found to be invalid

    Returns:
        User: Returns the user object that has been added to the database
    """
    try:
        is_valid = validate_email(_user.email)
        email = is_valid.email
    except EmailNotValidError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Provide valid email")

    hashed_password = hash.bcrypt.hash(_user.password)

    user_object = UserModel(
        email, _user.name,
        _user.phone_number,
        hashed_password
    )

    _db.add(user_object)
    _db.commit()
    _db.refresh(user_object)

    return user_object
