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


class UserRequest(UserBase):
    """Created the UserRequest class 

    Args:
        UserBase (Class): The parent class
    """
    password: str
