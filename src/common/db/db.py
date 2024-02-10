from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from config import URL

engine = create_engine(URL)
postgres_session_maker = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


def get_session():
    session = postgres_session_maker()
    try:
        yield session
    finally:
        session.close()
