from sqlalchemy import MetaData, Table
from app.database.database import engine

metadata = MetaData()

def get_table(table_name, schema=None):
    return Table(
        table_name,
        metadata,
        schema=schema,
        autoload_with=engine
    )