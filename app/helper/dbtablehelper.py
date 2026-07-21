from app.dbfunctions.dbtablesfunctions import getDBTableData

def getDBTables(dbps):
    dbtbl_data = getDBTableData(dbps)
    dbtbls = []
    for dbtbl in dbtbl_data:
        row = {
            "table_id": dbtbl.table_id,
            "table_name": dbtbl.table_name,
            "table_alias": dbtbl.table_alias
        }
        dbtbls.append(row)
    return dbtbls
    