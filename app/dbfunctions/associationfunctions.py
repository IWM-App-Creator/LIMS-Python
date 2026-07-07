from sqlalchemy import func
from app.utils.common import select, DB
from app.properties.associationproperties import associationps

def getAssociationData():
    association = DB.getTableMeta("sys_associations").alias("a")
    stmt = select(association)
    if associationps.association_id.get() not in (None, "", 0):
        stmt = stmt.where(association.c.associations_id == associationps.association_id.get())
    stmt = stmt.where(association.c.is_delete == 0)
    return stmt

def getDesignationData():
    designation = DB.getTableMeta("sys_designation").alias("d")
    stmt = select(designation)
    if associationps.designation_id.get() not in (None, "", 0):
        stmt = stmt.where(designation.c.designation_id == associationps.designation_id.get())
    stmt = stmt.where(designation.c.is_delete == 0)
    return stmt

def getAssociationUsers():
    assousers = DB.getTableMeta("sys_association_users").alias("au")
    stmt = select(assousers)
    if associationps.associations_id.get() not in (None, "", 0):
        stmt = stmt.where(assousers.c.associations_id == associationps.associations_id.get())
    if associationps.designation_id.get() not in (None, "", 0):
        stmt = stmt.where(assousers.c.designation_id == associationps.designation_id.get())
    if associationps.view_id.get() not in (None, "", 0):
        stmt = stmt.where(func.find_in_set(associationps.view_id.get(), assousers.c.dyncviews) > 0)
    if associationps.custlink.get() not in (None, "", 0):
        stmt = stmt.where(func.find_in_set(associationps.custlink.get(), assousers.c.custlink) > 0)
    if associationps.user_id.get() not in (None, "", 0):
        stmt = stmt.where(assousers.c.user_id == associationps.user_id.get())
    if associationps.col_id.get() not in (None, "", 0):
        stmt = stmt.where(assousers.c.col_id == associationps.col_id.get())
    if associationps.col_p_val.get() not in (None, "", 0):
        stmt = stmt.where(assousers.c.col_p_val == associationps.col_p_val.get())
    stmt = stmt.where(assousers.c.is_delete == 0)
    stmt = stmt.order_by(assousers.c.srno.asc())
    return DB.executeDBSelect(stmt)

def getAssociationViews():
    assoviews = DB.getTableMeta("sys_association_view").alias("av")
    stmt = select(assoviews)
    if associationps.view_id.get() not in (None, "", 0):
        stmt = stmt.where(assoviews.c.view_id == associationps.view_id.get())
    view_ids = associationps.view_ids.get()
    if view_ids not in (None, "", 0):
        view_id_list = [int(x) for x in view_ids.split(",") if x.strip()]
        stmt = stmt.where(assoviews.c.view_id.in_(view_id_list))
    stmt = stmt.where(assoviews.c.is_delete == 0)
    return stmt

def getAssociationDesignation():
    asso_designation = DB.getTableMeta("sys_assoc_designation").alias("ad")
    stmt = select(asso_designation)
    if associationps.associations_id.get() not in (None, "", 0):
        stmt = stmt.where(asso_designation.c.associations_id == associationps.associations_id.get())
    if associationps.designation_id.get() not in (None, "", 0):
        stmt = stmt.where(asso_designation.c.designation_id == associationps.designation_id.get())
    stmt = stmt.where(asso_designation.c.is_delete == 0)
    return stmt    