from app.utils.common import DB, select, or_, func, and_

def getActionList(actionps):
    view_id = int(actionps.view_id.get() or 0)
    pgno = int(actionps.pg_no.get() or 1)
    dync_actions = DB.getTableMeta("sys_dynamic_actions").alias("da")
    stmt = select(dync_actions)
    if actionps.search_text.get() not in (None, ""):
        stmt = stmt.where(dync_actions.c.action_name.like(f"%{actionps.search_text.get()}%"))
    if actionps.action_type.get() not in (None, ""):
        stmt = stmt.where(dync_actions.c.action_type == actionps.action_type.get())
    stmt = stmt.where(dync_actions.c.is_delete == 0)
    if view_id > 0:
        playground = DB.getTableMeta("sys_playground").alias("pg")
        storeprocedures = DB.getTableMeta("sys_storeprocedures").alias("sp")
        endpoints = DB.getTableMeta("sys_intg_endpoints").alias("ie")
        play_actions = DB.getTableMeta("sys_dynamic_actions").alias("pa")
        store_actions = DB.getTableMeta("sys_dynamic_actions").alias("sa")
        endpoint_actions = DB.getTableMeta("sys_dynamic_actions").alias("ea")
        view = DB.getTableMeta("sys_new_dynamic_view").alias("v")
        dbcols = DB.getTableMeta("sys_new_db_tables_cols").alias("db")
        viewcols = DB.executeDBSelectSingle(select(view.c.view_cols).where(view.c.view_id == view_id))
        col_ids = []
        if viewcols and viewcols.view_cols:
            col_ids = [item["col_id"] for item in viewcols.view_cols]
        playground_subqry = (
            select(play_actions.c.action_id)
            .join(
                playground,
                playground.c.playground_id
                == func.json_unquote(
                    func.json_extract(play_actions.c.action_json, "$.playground_id")
                ),
            )
            .where(playground.c.view_id == view_id)
        )

        storeproc_subq = (
            select(store_actions.c.action_id)
            .join(
                storeprocedures,
                storeprocedures.c.storeprocedure_id
                == func.json_unquote(
                    func.json_extract(store_actions.c.action_json, "$.storeprocedure_id")
                ),
            )
            .where(func.find_in_set(view_id, storeprocedures.c.view_ids))
        )

        endpoint_subq = (
            select(endpoint_actions.c.action_id)
            .join(
                endpoints,
                endpoints.c.endpoint_id
                == func.json_unquote(
                    func.json_extract(endpoint_actions.c.action_json, "$.endpoint_id")
                ),
            )
            .where(func.find_in_set(view_id, endpoints.c.view_ids))
        )

        stmt = stmt.where(
            or_(
                dync_actions.c.action_type == "System",
                dync_actions.c.action_id.in_(playground_subqry),
                dync_actions.c.action_id.in_(storeproc_subq),
                dync_actions.c.action_id.in_(endpoint_subq),
            )
        )

        if col_ids:
            column_count = (
                select(func.count(func.distinct(dbcols.c.col_name)))
                .where(
                    dbcols.c.col_id.in_(col_ids),
                    dbcols.c.col_name.in_(["sow_id", "coc_id", "project_id"])
                )
                .scalar_subquery()
            )
            stmt = stmt.where(
                or_(
                    dync_actions.c.action_id != 7,
                    column_count == 3
                )
            )
        else:
            stmt = stmt.where(dync_actions.c.action_id != 7)
    record_qry = select(func.count()).select_from(stmt.subquery())
    actionps.record_cnt.set(DB.executeDBScalar(record_qry))
    stmt = stmt.order_by(dync_actions.c.action_id.asc())
    stmt = stmt.offset((pgno - 1) * 9).limit(9)
    return DB.executeDBSelect(stmt)