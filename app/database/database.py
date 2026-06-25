import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

DATABASE_URL = (
    f"mysql+pymysql://{os.getenv('DB_USERNAME')}:"
    f"{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:"
    f"{os.getenv('DB_PORT')}/"
    f"{os.getenv('DB_DATABASE')}"
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    echo=False
)