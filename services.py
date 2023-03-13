"""A script meant to contain all the services logic"""
import os

from jwt import encode
from dotenv import find_dotenv, load_dotenv
from email_validator import EmailNotValidError, validate_email
from fastapi import HTTPException, status
from passlib import hash as _hash
from sqlalchemy import orm

from database import base, engine, session_local
from models import UserModel
from schemas import UserBase, UserRequest

load_dotenv(find_dotenv())

jwt_secret = os.environ.get("JWT_SECRET")


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
    except EmailNotValidError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"{e}+ Provide valid email")

    hashed_password = _hash.bcrypt.hash(_user.password)

    user_object = UserModel(
        email, _user.name,
        _user.phone_number,
        hashed_password
    )

    _db.add(user_object)
    _db.commit()
    _db.refresh(user_object)

    return user_object


async def create_token(user: UserModel) -> dict:
    """Created the create_token function

    Args:
        user (UserModel): The template of the user

    Returns:
        dict: A dictionary of the access_token and the token type
    """
    # Convert user model to user schema
    user_schema = UserBase.from_orm(user)
    # Converting the object to a dictionary
    user_dict = user_schema.dict()

    del user_dict["created_at"]

    token = encode(user_dict, jwt_secret, algorithm="HS256")

    return dict(access_token=token, token_type="bearer")
