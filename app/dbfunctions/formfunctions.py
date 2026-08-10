from app.utils.common import DB, select

def getFormDataDB(formps):
    form_id = int(formps.form_id.get() or 0)
    dync_form = DB.getTableMeta("sys_new_dynamic_form").alias("form")
    stmt = (
        select(dync_form)
        .where(dync_form.c.form_id == form_id)
        .where(dync_form.c.is_delete == 0)
    )
    return DB.executeDBSelectSingle(stmt)