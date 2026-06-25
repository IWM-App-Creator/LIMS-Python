import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_DATABASE = os.getenv("DB_DATABASE")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
MYSQL_ATTR_SSL_CA = os.getenv("MYSQL_ATTR_SSL_CA")


DATABASE_URL = (f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}"f"@{DB_HOST}:{DB_PORT}/{DB_DATABASE}")

connect_args = {}

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    echo=False,  # SQL logging
    connect_args=connect_args
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        # print("Database session opened")
        yield db
    finally:
        # print("Database session closed")
        db.close()