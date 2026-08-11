from app.utils.common import DB, select, insert, update, String, func, exists, and_, case, literal, nowWithTimeZone, userps

def getViewFiltersDB(filterps):
    view_id = int(filterps.view_id.get() or 0)
    user_id = int(userps.user_id.get() or 0)

    tbl_saved = DB.getTableMeta("sys_dynamic_result_save").alias("sdrs")
    tbl_widget = DB.getTableMeta("sys_widget_master").alias("swm")
    user_dashboard = DB.getTableMeta("sys_user_dashboard").alias("dash")

    widget_list_exists = (
        func.json_contains(
            user_dashboard.c.widget_list,
            func.json_object(
                "sys_widget_id",
                func.cast(
                    tbl_widget.c.sys_widget_id,
                    String
                )
            )
        ) == 1
    )

    exists_subquery = exists(
        select(1)
        .select_from(
            tbl_widget.join(
                user_dashboard,
                widget_list_exists
            )
        )
        .where(
            func.json_extract(
                tbl_widget.c.widget_json,
                "$.view_id"
            ) == view_id,

            func.json_extract(
                tbl_widget.c.widget_json,
                "$.save_id"
            ) == tbl_saved.c.save_id,

            tbl_widget.c.view_id == view_id,

            tbl_widget.c.is_delete == 0,

            user_dashboard.c.created_by == user_id
        )
    )

    widget_added = case(
        (
            exists_subquery,
            literal(1)
        ),
        else_=literal(0)
    ).label("widget_added")

    stmt = (
        select(
            tbl_saved,
            widget_added
        )
        .where(
            tbl_saved.c.view_id == view_id,
            tbl_saved.c.is_delete == 0,
            tbl_saved.c.created_by == user_id
        )
    )

    return DB.executeDBSelect(stmt)

def getFilterData(filterps):
    save_id = int(filterps.save_id.get() or 0)
    tbl_saved = DB.getTableMeta("sys_dynamic_result_save").alias("sdrs")
    stmt = select(tbl_saved)
    stmt = stmt.where(tbl_saved.c.save_id == save_id)
    return DB.executeDBSelectSingle(stmt)

def getUserDefaultFilter(filterps):
    view_id = int(filterps.view_id.get() or 0)
    user_id = userps.user_id.get()
    tbl_saved = DB.getTableMeta("sys_dynamic_result_save").alias("sdrs")
    stmt = select(tbl_saved)
    stmt = stmt.where(tbl_saved.c.view_id == view_id)
    stmt = stmt.where(tbl_saved.c.is_default == 1)
    stmt = stmt.where(tbl_saved.c.created_by == user_id)
    stmt = stmt.where(tbl_saved.c.is_delete == 0)
    return DB.executeDBSelectSingle(stmt)

def insertUpdateFilter(filterps):
    user_id = userps.user_id.get()
    if filterps.user_id.get() not in (None, "", 0):
        user_id = filterps.user_id.get()
    save_id = int(filterps.save_id.get() or 0)
    save_name = filterps.save_name.get()
    view_id = int(filterps.view_id.get() or 0)
    view_qry = filterps.view_qry.get()
    view_qry_json = filterps.view_qry_json.get()
    is_default = int(filterps.is_default.get() or 0)
    is_delete = int(filterps.is_delete.get() or 0)
    values = {}
    if filterps.upd_vals.get() not in (None, "", {}):
        values = filterps.upd_vals.get()
    else:
        if save_name not in (None, ""):
            values['save_name'] = save_name
        if view_id not in (None, "", 0):
            values['view_id'] = view_id
        if view_qry not in (None, ""):
            values['view_qry'] = view_qry
        if view_qry_json not in (None, "", []):
            values['view_qry_json'] = view_qry_json
        if is_default not in (None, ""):
            values['is_default'] = is_default
        if is_delete not in (None, ""):
            values['is_delete'] = is_delete
    dync_result_save = DB.getTableMeta("sys_dynamic_result_save")
    if is_default in (1, "1") or save_id in (-1, "-1"):
        stmt = update(dync_result_save).where(dync_result_save.c.view_id == view_id).where(dync_result_save.c.created_by == user_id).values(is_default = 0)
        DB.executeDBUpdate(stmt)
    if save_id not in (-1, "-1"):
        if save_id not in (None, "", 0):
            stmt = update(dync_result_save).where(dync_result_save.c.save_id == save_id).values(**values)
            DB.executeDBUpdate(stmt)
        else:
            values['created_by'] = user_id
            values['tab_id'] = 0
            values['is_global'] = 0
            values['created_date'] = nowWithTimeZone()
            stmt = insert(dync_result_save).values(**values)
            save_id = DB.executeDBInsert(stmt)
    return save_id