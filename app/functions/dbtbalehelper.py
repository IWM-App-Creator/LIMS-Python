from sqlalchemy import func
from app.utils.common import select, DB, userps
from app.dbfunctions.dbtablesfunctions import getDBTableData

def getPrimaryKeyByTableID(dbps):
    db_tbl_data = getDBTableData(dbps)
    return db_tbl_data
    # print(db_tbl_data.col_id)
    # is_primary = dbps.is_primary.get()
    # dbps.db_tbl_data.set( DB.executeDBSelect(stmt) )

def getPrimaryKeyByTableNM(dbps):
    db_tbl_data = getDBTableData(dbps)
    return db_tbl_data
    # print(db_tbl_data.col_id)
    # is_primary = dbps.is_primary.get()
    # dbps.db_tbl_data.set( DB.executeDBSelect(stmt) )