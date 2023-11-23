"""
This module provides functions for initializing the database engine and creating a session factory.

The database engine is responsible for connecting to the database and managing the database
connection. The session factory is used to create database sessions, which are used to interact
with the database.

Example usage:
    binding_engine = init_engine()
    session_factory = get_session_factory(binding_engine)
    session = session_factory()
"""
from server.database import SessionMaker, Engine, create_engine, DB_PATH
from server.models import Base

DATABASE_URL: str = f"sqlite:///{DB_PATH}/database.db"

def init_engine() -> Engine:
    """
    Initializes the database engine.

    Returns:
        The initialized database engine.
    """
    print(DATABASE_URL)
    binding_engine: Engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(binding_engine)
    return binding_engine

def get_session_factory(binding_engine: Engine) -> SessionMaker:
    """
    Returns a session factory for creating database sessions.

    Args:
        binding_engine (engine): The database engine to bind the session to.

    Returns:
        sessionmaker: A session factory object.

    """
    return SessionMaker(bind=binding_engine)
