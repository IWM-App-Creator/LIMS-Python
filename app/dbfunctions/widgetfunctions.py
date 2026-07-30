from app.utils.common import DB, select, case, literal, exists, and_, userps

def getWidgetsDB(widgetps):
    dashboard_id = int(widgetps.dashboard_id.get() or 0)
    sys_widget_cat_id = int(widgetps.sys_widget_cat_id.get() or 0)
    search_text = widgetps.search_text.get()
    widget_type = widgetps.widget_type.get()
    view_id = int(widgetps.view_id.get() or 0)
    tbl_widget = DB.getTableMeta("sys_widget_master").alias("wm")
    tbl_view = DB.getTableMeta("sys_new_dynamic_view").alias("dv")
    tbl_user_widget = DB.getTableMeta("sys_user_widgets").alias("suw")
    # EXISTS subquery
    exists_conditions = [
        tbl_user_widget.c.sys_widget_id == tbl_widget.c.sys_widget_id,
        tbl_user_widget.c.user_id == userps.user_id.get(),
        tbl_user_widget.c.is_delete == 0,
    ]
    if dashboard_id not in (None, "", 0):
        exists_conditions.append(
            tbl_user_widget.c.dashboard_id == dashboard_id
        )
    widget_added = case(
        (
            tbl_widget.c.is_multiple == 1,
            literal(0)
        ),
        (
            exists(
                select(1).where(and_(*exists_conditions))
            ),
            literal(1)
        ),
        else_=literal(0)
    ).label("widget_added")
    stmt = (
        select(
            tbl_widget,
            tbl_view.c.view_name,
            tbl_view.c.url,
            widget_added
        )
        .outerjoin(
            tbl_view,
            tbl_view.c.view_id == tbl_widget.c.view_id
        )
    )
    # Filters
    if sys_widget_cat_id:
        stmt = stmt.where(tbl_widget.c.sys_widget_cat_id == sys_widget_cat_id)

    if search_text:
        stmt = stmt.where(tbl_widget.c.widget_title.like(f"%{search_text}%"))

    if widget_type:
        stmt = stmt.where(tbl_widget.c.widget_type == widget_type)

    if view_id:
        stmt = stmt.where(tbl_widget.c.view_id == view_id)

    if userps.role_id.get() != 1 and userps.ws_role_id.get() != 1:
        stmt = stmt.where(
            tbl_widget.c.widget_type.notin_(["ADDUSER", "ADDVIEW"])
        )
    stmt = stmt.where(
        and_(
            (
                (tbl_widget.c.created_by == userps.user_id.get()) |
                (tbl_widget.c.is_system == 1) |
                (tbl_widget.c.is_global == 1)
            ),
            tbl_widget.c.is_delete == 0
        )
    )
    stmt = (
        stmt.order_by(
            tbl_widget.c.is_system.desc(),
            tbl_widget.c.sys_widget_id.asc()
        )
    )
    return DB.executeDBSelect(stmt)

def getUserWidgetsDB(widgetps):
    preview = int(widgetps.preview.get() or 0)
    dashboard_id = int(widgetps.dashboard_id.get() or 0)
    widget_id = int(widgetps.sys_widget_id.get() or 0)
    tbl_widget = DB.getTableMeta("sys_widget_master").alias("wm")
    tbl_user_widget = DB.getTableMeta("sys_user_widgets").alias("uw")
    stmt = (
        select(
            tbl_widget,
            tbl_user_widget.c.sys_widgets_users_id,
            tbl_user_widget.c.c_width,
            tbl_user_widget.c.c_height,
            tbl_user_widget.c.htm_flow,
            tbl_user_widget.c.bg_color,
            tbl_user_widget.c.widget_label,
            tbl_user_widget.c.widget_setting
        )
        .outerjoin(
            tbl_user_widget,
            tbl_user_widget.c.sys_widget_id == tbl_widget.c.sys_widget_id
        )
        .where(
            tbl_widget.c.is_delete == 0,
            tbl_user_widget.c.is_delete == 0
        )
    )
    if preview == 0:
        stmt = stmt.where(
            tbl_user_widget.c.user_id == userps.user_id.get(),
            tbl_user_widget.c.dashboard_id == dashboard_id
        )
    if widget_id not in (None, "", 0):
        stmt = stmt.where(
            tbl_user_widget.c.sys_widgets_users_id == widget_id
        )
    stmt = stmt.order_by(tbl_user_widget.c.rank.asc())
    return DB.executeDBSelect(stmt)