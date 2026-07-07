from sqlalchemy import MetaData, Table, text
from app.dbhelper.database import dbconn
from app.properties.usersproperties import userps
import re

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
    def getSingleColumnValue(stmt, column_name, default = None):
        row = DB.executeDBSelectSingle(stmt)
        return getattr(row, column_name, default) if row else default

    def executeDBStatement(stmt):
        with dbconn.begin() as conn:
            schema_name = userps.schema_name.get()
            if schema_name:
                conn.execute(text(f"USE `{schema_name}`"))
            if isinstance(stmt, str):
                stmt = text(stmt)
            result = conn.execute(stmt)
            return result.fetchall()

    @staticmethod
    def getRecordCount(stmt):
        with dbconn.begin() as conn:
            # schema_name = userps.schema_name.get()
            # if schema_name:
            #     conn.execute(text(f"USE `{schema_name}`"))
            # if not isinstance(stmt, str):
            #     stmt = str(stmt)
            # stmt = re.sub(
            #     r"\s+LIMIT\s+\d+(\s*,\s*\d+)?\s*;?\s*$",
            #     "",
            #     stmt,
            #     flags = re.IGNORECASE
            # )
            # count_stmt = text(
            #     f"SELECT COUNT(*) AS total_count FROM ({stmt}) AS tmp"
            # )
            # result = conn.execute(count_stmt)
            # return result.scalar() or 0
            schema_name = userps.schema_name.get()

            if schema_name:
                conn.execute(text(f"USE `{schema_name}`"))

            if not isinstance(stmt, str):
                stmt = str(stmt)

            # Remove LIMIT clause
            stmt = re.sub(
                r"\s+LIMIT\s+\d+(\s*,\s*\d+)?\s*;?\s*$",
                "",
                stmt,
                flags=re.IGNORECASE
            )

            # Remove ORDER BY clause (last occurrence)
            stmt = re.split(r"\border\s+by\b", stmt, flags=re.IGNORECASE)[0]

            # Find the FROM clause
            match = re.search(r"\bfrom\b", stmt, flags=re.IGNORECASE)

            if not match:
                return 0

            count_qry = f"SELECT COUNT(*) AS rcdcnt {stmt[match.start():]}"
            print("count_qry --> ", count_qry)
            result = conn.execute(text(count_qry))
            return result.scalar() or 0
