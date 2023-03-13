"""This file is going to hold all the models for the app"""
from datetime import datetime

import sqlalchemy.orm
from passlib import hash
from sqlalchemy import Column, DateTime, Integer, String, ForeignKey

from database import base, session_local


class UserModel(base):
    """The template for the User data

    Args:
        base (Class): The parent class for the UserModel
    """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    phone_number = Column(String)
    password_hash = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow())


class PostModel(base):
    """CReated the model for the Post item

    Args:
        base (Class): The parent class
    """
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    post_title = Column(String, index=True)
    post_body = Column(String, index=True)
    post_description = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.utcnow())
