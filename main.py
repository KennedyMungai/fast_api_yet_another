"""The entry point to the program"""
from typing import List

from fastapi import Depends, FastAPI, HTTPException, Security, status
from sqlalchemy import orm

from schemas import PostRequest, PostResponse, UserRequest, UserResponse
from services import create_post as _create_post
from services import create_token, create_user
from services import current_user as _current_user
from services import get_db
from services import get_post_detail as _get_post_by_detail
from services import get_posts_by_user as _get_posts_by_user
from services import get_user_by_email, login
from services import delete_post as _delete_post
from services import update_post as _update_post
from services import get_posts_by_all_users as _get_posts_by_all_users

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
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    _db: orm.Session = Depends(get_db)
):
    """Defined the function for the login endpoint

    Args:
        form_data (OAuth2PasswordRequestForm, optional): Contains the email 
                                                        and the password. Defaults to Depends().
        db (orm.Session, optional): The database session. Defaults to Depends(get_db).

    Raises:
        HTTPException: An unauthorized exception is raised incase of false login credentials

    Returns:
        Token: Creates and returns a token for the user
    """
    db_user = await login(form_data.username, form_data.password, _db)

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong login credentials")

    return await create_token(db_user)


@app.get("/api/users/currentuser", response_model=UserResponse)
async def current_user(_user: UserResponse = Depends(_current_user)):
    """An endpoint to get the current user of the application

    Args:
        _user (UserResponse, optional): The template for the User 
                                        data. Defaults to Depends(_current_user).

    Returns:
        User: The user data template
    """
    return _user


@app.post("/api/v1/posts", response_model=PostResponse)
async def create_post(
        _post_request: PostRequest,
        _user: UserRequest = Depends(_current_user),
        _db: orm.Session = Depends(get_db)
):
    """An endpoint for creating posts

    Args:
        _post_request (PostRequest): The Post data
        _user (UserRequest, optional): The user creating the post. Defaults to Depends(_current_user).
        _db (orm.Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        _type_: _description_
    """
    return await _create_post(_user, _db, _post_request)


@app.get("/api/v1/posts/user", response_model=List[PostResponse])
async def get_posts_by_user(_user: UserRequest, _db: orm.Session = Depends(get_db)) -> list:
    """The API endpoint to get all the posts by a specific

    Args:
        _user (UserRequest): The user
        _db (orm.Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        list: A list of all the posts by a specific user
    """
    return await _get_posts_by_user(_user, _db)


@app.get("/api/v1/posts/all", response_model=List[PostResponse])
async def get_posts_by_all_users(_db: orm.Session = Depends(get_db)) -> list:
    """The API endpoint to get all the posts by a specific

    Args:
        _user (UserRequest): The user
        _db (orm.Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        list: A list of all the posts by a specific user
    """
    return await _get_posts_by_all_users(_db)


@app.get("/api/posts/{post_id}", response_model=PostResponse)
async def get_post_detail(post_id: int, _db: orm.Session = Depends(get_db)):
    """Defined the endpoint to get the details of a specific post

    Args:
        post_id (int): The id of the post
        _db (orm.Session, optional): The database session. Defaults to Depends(get_db).

    Raises:
        HTTPException: A not found exception is raised when the post is not found

    Returns:
        _type_: The post is returned
    """
    post = await _get_post_by_detail(post_id, _db)

    return post


@app.delete("/api/v1/posts/{post_id}")
async def delete_post(post_id: int, _db: orm.Session = Depends(get_db), _user: UserRequest = Depends(current_user)) -> str:
    """The endpoint to delete a post

    Args:
        post_id (int): The id of the post
        _db (orm.Session, optional): The database session. Defaults to Depends(get_db).
        _user (UserRequest, optional): The User. Defaults to Depends(current_user).

    Returns:
        str: A message to show successful deletion of the post
    """
    post = await _get_post_by_detail(post_id, _db)
    await _delete_post(post, _db)

    return "Post deleted"


@app.put("/api/v1/posts/{post_id}", response_model=PostResponse)
async def update_post(post_id: int, _post_request: PostRequest, _db: orm.Session = Depends(get_db)):
    """The update post endpoint

    Args:
        post_id (int): The id of teh post
        _post_request (PostRequest): The template for te post request data
        _db (orm.Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        _type_: _description_
    """
    db_post = await _get_post_by_detail(post_id, _db)

    return await _update_post(_post_request, db_post, _db)
