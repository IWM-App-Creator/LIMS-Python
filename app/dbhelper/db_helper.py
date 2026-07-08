from sqlalchemy import MetaData, Table, text
from app.dbhelper.database import dbconn
from app.properties.usersproperties import userps

metadata = MetaData()

class DB:

    _dbtables = {}

    @staticmethod
    def getTableMeta(table_name, schema = None):
        if schema is None: # If Schema name is not pass, use form User Property
            schema = userps.schema_name.get()
        key = f"{schema}.{table_name}" if schema else table_name
        if key not in DB._dbtables:
            DB._dbtables[key] = Table (
                table_name,
                metadata,
                schema = schema,
                autoload_with = dbconn
            )
        return DB._dbtables[key]

    @staticmethod
    def executeDBSelect(stmt):
        with dbconn.connect() as conn:
            result = conn.execute(stmt)
            return result.fetchall()

    @staticmethod
    def executeDBSelectSingle(stmt):
        with dbconn.connect() as conn:
            result = conn.execute(stmt)
            return result.first()

    @staticmethod
    def executeDBInsert(stmt):
        with dbconn.begin() as conn:
            result = conn.execute(stmt)
            if result.inserted_primary_key:
                return result.inserted_primary_key[0]

            return None

    @staticmethod
    def executeDBUpdate(stmt):
        with dbconn.begin() as conn:
            result = conn.execute(stmt)
            return result.rowcount

    @staticmethod
    def executeDBDelete(stmt):
        with dbconn.begin() as conn:
            result = conn.execute(stmt)
            return result.rowcount

    @staticmethod
    def getSingleColumnValue(stmt, column_name, default = None):
        if isinstance(stmt, str):
                stmt = text(stmt)
        row = DB.executeDBSelectSingle(stmt)
        return getattr(row, column_name, default) if row else default

    @staticmethod
    def executeDBStatement(stmt):
        with dbconn.begin() as conn:
            schema_name = userps.schema_name.get()
            if schema_name:
                conn.execute(text(f"USE `{schema_name}`"))
            if isinstance(stmt, str):
                stmt = text(stmt)
            result = conn.execute(stmt)
            return result.fetchall()
