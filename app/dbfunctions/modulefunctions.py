from app.utils.common import select, update, insert, or_, DB, userps, nowWithTimeZone

def getViewModulesData(moduleps):
    db_templates = DB.getTableMeta("db_templates", "systemconfig").alias("dt")
    stmt = select(db_templates)
    if moduleps.template_type.get() not in (None, ""):
        stmt = stmt.where(db_templates.c.template_type == moduleps.template_type.get())
    if moduleps.t_cat_id.get() not in (None, ""):
        stmt = stmt.where(db_templates.c.t_cat_id == moduleps.t_cat_id.get())
    stmt = stmt.where(db_templates.c.is_delete == 0)
    return DB.executeDBSelect(stmt)