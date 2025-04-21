from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from .util_logger import logger

SQLALCHEMY_DATABASE_URL = "sqlite:///./users.db"

try:
    logger.info("Creating database engine with SQLite")
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
    logger.info("Database engine created successfully.")
    Base = declarative_base()
    logger.info("Creating Session to database")
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    logger.info("Database Session created successfully.")
except Exception as e:
    logger.error(f"An error occurred while creating the engine: {e}", exc_info=True)
    raise


def get_db():
    logger.info("Opening DB session")
    db = SessionLocal()
    try:
        yield db
    finally:
        logger.info("Closing DB session")
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

try:
    logger.info("Creating Database tables")
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created succesfully")
except Exception as e:
    logger.error(f"An error occurred while creating the tables: {e}", exc_info=True)
    raise
