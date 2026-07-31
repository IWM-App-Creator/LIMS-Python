from app.utils.common import DB, select, func, exists, and_, case, literal, userps

def getViewFiltersDB(filterps):
    dync_result_save = DB.getTableMeta("sys_dynamic_result_save").alias("dr")
    stmt = select(dync_result_save)
    if filterps.save_id.get() not in (None, "", 0):
        stmt = stmt.where(dync_result_save.c.save_id == filterps.save_id.get())
    if filterps.view_id.get() not in (None, "", 0):
        stmt = stmt.where(dync_result_save.c.view_id == filterps.view_id.get())
    if filterps.is_default.get() not in (None, "", 0):
        stmt = stmt.where(dync_result_save.c.is_default == filterps.is_default.get())
    stmt = stmt.where(dync_result_save.c.is_delete == 0)
    stmt = stmt.order_by(dync_result_save.c.save_id.asc())
    return DB.executeDBSelect(stmt)

def getViewFiltersDB(filterps):
    view_id = filterps.view_id.get()
    tbl_saved = DB.getTableMeta("sys_dynamic_result_save").alias("sdrs")
    tbl_widget = DB.getTableMeta("sys_widget_master").alias("swm")
    tbl_user_widget = DB.getTableMeta("sys_user_widgets").alias("suw")
    pattern = func.concat('%{"view_id":"', str(view_id), '","save_id":"', tbl_saved.c.save_id, '"%')
    exists_subquery = (
        exists(
            select(1)
            .select_from(
                tbl_widget.join(
                    tbl_user_widget,
                    and_(
                        tbl_user_widget.c.sys_widget_id == tbl_widget.c.sys_widget_id,
                        tbl_user_widget.c.is_delete == 0
                    )
                )
            )
            .where(
                tbl_widget.c.widget_json.like(pattern),
                tbl_widget.c.view_id == view_id,
                tbl_widget.c.is_delete == 0
            )
        )
    )
    widget_added = case((exists_subquery, literal(1)), else_=literal(0)).label("widget_added")
    stmt = (
        select(
            tbl_saved,
            widget_added
        )
        .where(
            tbl_saved.c.view_id == view_id,
            tbl_saved.c.is_delete == 0,
            tbl_saved.c.created_by == userps.user_id.get()
        )
    )
    return DB.executeDBSelect(stmt)