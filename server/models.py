"""
This file contains the SQLAlchemy models for the database.
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase

#pylint: disable=too-few-public-methods

class Base(DeclarativeBase):
    """
    Base class for all models.
    """

class User(Base):
    """
    User model. Contains the username and password of a user.
    """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
