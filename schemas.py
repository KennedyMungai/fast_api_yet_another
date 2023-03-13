"""The schemas script"""
from datetime import datetime

from pydantic import BaseModel


class UserBase(BaseModel):
    """Created the UserBase model

    Args:
        BaseModel (Class): The parent class
    """
    email: str
    name: str
    phone_number: str

    class Config:
        """Config for the UserBase class"""
        orm_mode = True


class UserRequest(UserBase):
    """Created the UserRequest class 

    Args:
        UserBase (Class): The parent class
    """
    password: str

    class Config:
        """Config for the UserRequest class"""
        orm_mode = True


class UserResponse(UserBase):
    """The template for the User response data

    Args:
        UserBase (Class): The parent class
    """
    id: int
    created_at: datetime

    class Config:
        """Config for the UserResponse class"""
        orm_mode = True


class PostBase(BaseModel):
    """The Post base model

    Args:
        BaseModel (Class): The parent class
    """
    post_title: str
    post_description: str
    image: str


class PostRequest(PostBase):
    """The template for the Post Request data

    Args:
        PostBase (Class): The parent class
    """
    pass


class PostResponse(PostBase):
    """The Template for th Post response 

    Args:
        PostBase (Class): The parent class
    """
    id: int
    user_id: str
    created_at: datetime
