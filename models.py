"""This file is going to hold all the models for the app"""
from datetime import datetime

import sqlalchemy.orm
from passlib import hash
from sqlalchemy import Column, DateTime, Integer, String

from database import base, session_local


class UserModel(base):
    """The template for the User data

    Args:
        base (Class): The parent class for the UserModel
    """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow())
