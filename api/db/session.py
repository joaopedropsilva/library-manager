import logging
from typing import Generator

from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError

from api.core.config import settings


logger = logging.getLogger(__name__)

_engine = None
_SessionDB = None


def setup_db():
    logger.debug(f"Setting up database with URL: {settings.database_url}")
    _engine = create_engine(settings.database_url)
    _SessionDB = sessionmaker(autocommit=False, autoflush=False, bind=_engine)


def get_session() -> Generator[Session, None, None]:
    with _SessionDB() as session:
        try:
            yield session
        except SQLAlchemyError:
            logger.exception(f"Failed on database operation")
            session.rollback()
