"""A script meant to contain all the services logic"""
import os

from jwt import encode, decode
from dotenv import find_dotenv, load_dotenv
from email_validator import EmailNotValidError, validate_email
from fastapi import HTTPException, status, Depends
from passlib import hash as _hash
from sqlalchemy import orm

from database import base, engine, session_local
from models import UserModel
from schemas import UserResponse, UserRequest

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
    except EmailNotValidError as _e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"{_e} Please provide valid email")

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
    user_schema = UserResponse.from_orm(user)
    # Converting the object to a dictionary
    user_dict = user_schema.dict()

    del user_dict["created_at"]

    token = encode(user_dict, jwt_secret, algorithm="HS256")

    return dict(access_token=token, token_type="bearer")


async def login(_email: str, _password: str, _db: orm.Session):
    """Defined the login function

    Args:
        _email (str): The email of the user
        _password (str): The password of the user
        _db (orm.Session): The database session

    Returns:
        _type_: _description_
    """
    db_user = await get_user_by_email(_email, _db)

    if not db_user:
        return False

    if not db_user.password_verification(_password):
        return False

    return db_user


async def current_user(
    _db: orm.Session = Depends(get_db),
    token: str = Depends(oauth2schema)
):
    """A function to get the current user

    Args:
        _db (orm.Session, optional): The database session. Defaults to Depends(get_db).
        token (str, optional): The access token for the application. Defaults to Depends().

    Raises:
        HTTPException: The unauthorized exception is raised incase of the wrong credentials

    Returns:
        _type_: _description_
    """
    try:
        payload = decode(token, jwt_secret, algorithms=["HS256"])
        # To get the user by Id and the Id is already available in the decoded user payload
        # along with the email, phone and name
        db_user = _db.query(UserModel).get(payload["id"])
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong credentials")

    return UserResponse.from_orm(_db)
