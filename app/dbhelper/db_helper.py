from sqlalchemy import MetaData, Table
from app.dbhelper.database import dbconn
from app.properties.globalproperties import globalps

metadata = MetaData()

class DB:

    _dbtables = {}

    @staticmethod
    def tableMeta(table_name):
        return DB.getTableMeta (
            table_name,
            globalps.schema_name
        )

    @staticmethod
    def getTableMeta(table_name, schema = None):
        key = f"{schema}.{table_name}" if schema else table_name
        if key not in DB._dbtables:
            DB._dbtables[key] = Table(
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
            return result.inserted_primary_key

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
    def executeDBStatement(stmt):
        with dbconn.begin() as conn:
            return conn.execute(stmt)