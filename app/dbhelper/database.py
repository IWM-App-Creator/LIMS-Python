import os
from sqlalchemy import create_engine

DATABASE_URL = (
    f"mysql+pymysql://{os.getenv('DB_USERNAME')}:"
    f"{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:"
    f"{os.getenv('DB_PORT')}/"
    f"{os.getenv('DB_DATABASE')}"
)

dbconn = create_engine (
    DATABASE_URL,
    pool_pre_ping = True,
    echo = False
)