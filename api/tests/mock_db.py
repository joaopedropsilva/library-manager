from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session


_engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_fake_session() -> Generator[Session, None, None]:
    with _session() as session:
        yield session
        session.close()
