from sqlalchemy import func
from app.utils.common import select, DB
from app.properties.associationproperties import associationps

def getAssociationData():
    association = DB.tableMeta("sys_associations")
    stmt = select(association)
    if associationps.association_id.get() not in (None, ""):
        stmt = stmt.where(association.c.associations_id == associationps.association_id.get())
    stmt = stmt.where(association.c.is_delete == 0)
    return DB.executeDBSelectSingle(stmt)