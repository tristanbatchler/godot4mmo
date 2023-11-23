"""
This module contains the database engine and session factory. The engine is used to connect to the
database and the session factory is used to create sessions to interact with the database.
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker as SessionMaker

DB_PATH: str = os.path.dirname(os.path.abspath(__file__))
