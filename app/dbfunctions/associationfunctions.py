from sqlalchemy import func
from app.utils.common import select, DB
from app.properties.associationproperties import associationps

def getAssociationData():
    association = DB.getTableMeta("sys_associations")
    stmt = select(association)
    if associationps.association_id.get() not in (None, "", 0):
        stmt = stmt.where(association.c.associations_id == associationps.association_id.get())
    stmt = stmt.where(association.c.is_delete == 0)
    return DB.executeDBSelectSingle(stmt)

def getDesignationData():
    designation = DB.getTableMeta("sys_designation")
    stmt = select(designation)
    if associationps.designation_id.get() not in (None, "", 0):
        stmt = stmt.where(designation.c.designation_id == associationps.designation_id.get())
    stmt = stmt.where(designation.c.is_delete == 0)
    return DB.executeDBSelectSingle(stmt)

def getAssociationUsers():
    assousers = DB.getTableMeta("sys_association_users")
    stmt = select(assousers)
    if associationps.associations_id.get() not in (None, "", 0):
        stmt = stmt.where(assousers.c.associations_id == associationps.associations_id.get())
    if associationps.designation_id.get() not in (None, "", 0):
        stmt = stmt.where(assousers.c.designation_id == associationps.designation_id.get())
    if associationps.user_id.get() not in (None, "", 0):
        stmt = stmt.where(assousers.c.user_id == associationps.user_id.get())
    if associationps.col_id.get() not in (None, "", 0):
        stmt = stmt.where(assousers.c.col_id == associationps.col_id.get())
    if associationps.col_p_val.get() not in (None, "", 0):
        stmt = stmt.where(assousers.c.col_p_val == associationps.col_p_val.get())
    stmt = stmt.where(assousers.c.is_delete == 0)
    print("stmt --> ", stmt)