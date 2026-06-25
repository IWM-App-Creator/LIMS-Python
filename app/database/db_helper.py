from sqlalchemy import MetaData, Table

metadata = MetaData()

def get_table(engine, table_name, schema=None):
    return Table(
        table_name,
        metadata,
        schema=schema,
        autoload_with=engine
    )