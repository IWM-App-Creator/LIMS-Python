from sqlalchemy import MetaData, Table
from app.database.database import dbconn

metadata = MetaData()

# To Get Table Data 
def get_table(table_name, schema = None):
    return Table(
        table_name,
        metadata,
        schema = schema,
        autoload_with = dbconn
    )