from typing import Generator

from sqlalchemy.engine import Engine, create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

engine: Engine = create_engine(
    "sqlite:///./thinky.db", connect_args={"check_same_thread": False}
)

SessionLocal: sessionmaker[Session] = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)

Base = declarative_base()


def init_db() -> None:
    """Initialize the database."""
    Base.metadata.create_all(bind=engine)


def get_db() -> Generator[Session, None, None]:
    """Dependency to get a database session.

    Yields:
        Session: A SQLAlchemy database session.
    """
    db: Session = SessionLocal()

    try:
        yield db
    # except Exception:
    #     db.rollback()
    finally:
        db.close()
