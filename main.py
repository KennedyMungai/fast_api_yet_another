"""The entry point to the program"""
from fastapi import Depends, FastAPI, HTTPException, status, Security
from sqlalchemy import orm

from schemas import UserRequest
from services import get_db, get_user_by_email, create_user, create_token, login

app = FastAPI()


@app.post("/api/v1/users")
async def register_user(_user: UserRequest, _db: orm.Session = Depends(get_db)):
    """Created the register user endpoint

    Args:
        _user (UserRequest): The template for the User data
        _db (orm.Session, optional): The database session. Defaults to Depends(get_db()).

    Raises:
        HTTPException: A bad request exception is raised if
                        the email address provided is found to not be valid

    Returns:
        token: A token is created based on the db_user
    """
    db_user = await get_user_by_email(_user.email, _db)

    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="The Email address provided is already in use")

    db_user = await create_user(_user, _db)

    return await create_token(db_user)


@app.post("/api/v1/login")
async def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: orm.Session = Depends(get_db)):
    """Defined the function for the login endpoint

    Args:
        form_data (OAuth2PasswordRequestForm, optional): Contains the email and the password. Defaults to Depends().
        db (orm.Session, optional): The database session. Defaults to Depends(get_db).

    Raises:
        HTTPException: An unauthorized exception is raised incase of false login credentials

    Returns:
        Token: Creates and returns a token for the user
    """
    db_user = await login(form_data.username, form_data.password, db)

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong login credentials")

    return await create_token(db_user)
