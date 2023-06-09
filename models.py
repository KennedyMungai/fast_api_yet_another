"""This file is going to hold all the models for the app"""
from datetime import datetime

from passlib import hash as _hash
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import base


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
    posts = relationship("PostModel", back_populates="user")

    def password_verification(self, password: str) -> bool:
        """A simple method to compare the entered password with the stored password

        Args:
            password (str): The entered password string

        Returns:
            bool: Whether the two strings match
        """
        return _hash.bcrypt.verify(password, self.password_hash)


class PostModel(base):
    """Created the model for the Post item

    Args:
        base (Class): The parent class
    """
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    post_title = Column(String, index=True)
    post_body = Column(String, index=True)
    image = Column(String)
    post_description = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.utcnow())
    user = relationship("UserModel", back_populates="posts")
