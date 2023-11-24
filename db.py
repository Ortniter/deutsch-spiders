from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import config

SQLALCHEMY_DATABASE_URL = config.DATABASE_URL

if config.HEROKU_ENV:
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace('postgres://', 'postgresql://', 1)
else:
    USER = config.POSTGRES_USER
    PASSWORD = config.POSTGRES_PASSWORD
    HOST = config.POSTGRES_HOST
    PORT = config.POSTGRES_PORT
    DATABASE = config.POSTGRES_DB
    SQLALCHEMY_DATABASE_URL = f'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
