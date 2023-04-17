import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session

DB_LOGIN = "nmap"
DB_PASSWORD = "nmap"
DB_HOST = "localhost"
DB_NAME = "nmap_scans"

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_LOGIN}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_recycle=300, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
