from app.utils.common import DB, select, insert, update, func, case, literal, exists, String, and_, nowWithTimeZone, userps

def getWidgetsDB(widgetps):
    dashboard_id = int(widgetps.dashboard_id.get() or 0)
    sys_widget_cat_id = int(widgetps.sys_widget_cat_id.get() or 0)
    search_text = widgetps.search_text.get()
    widget_type = widgetps.widget_type.get()
    view_id = int(widgetps.view_id.get() or 0)
    tbl_widget = DB.getTableMeta("sys_widget_master").alias("wm")
    tbl_view = DB.getTableMeta("sys_new_dynamic_view").alias("dv")
    # tbl_user_widget = DB.getTableMeta("sys_user_widgets").alias("suw")
    user_dashboard = DB.getTableMeta("sys_user_dashboard").alias("dash")
    # EXISTS subquery
    exists_conditions = [
        func.json_search(
            user_dashboard.c.widget_list,
            "one",
            func.cast(tbl_widget.c.sys_widget_id, String),
            None,
            "$[*].sys_widget_id"
        ).isnot(None)
    ]
    if dashboard_id not in (None, "", 0):
        exists_conditions.append(
            user_dashboard.c.dashboard_id == dashboard_id
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

def getWidgetData(widgetps):
    sys_widget_id = int(widgetps.sys_widget_id.get() or 0)
    sys_widget_ids = widgetps.sys_widget_ids.get()
    widget_type = widgetps.widget_type.get()
    view_id = int(widgetps.view_id.get() or 0)
    widget_json = widgetps.widget_json.get()
    created_by = int(widgetps.created_by.get() or 0)
    fetch_single = int(widgetps.fetch_single.get() or 0)
    widget_master = DB.getTableMeta("sys_widget_master").alias("wm")
    stmt = select(widget_master)
    if sys_widget_id not in (None, "", 0):
        stmt = stmt.where(widget_master.c.sys_widget_id == sys_widget_id)
    if sys_widget_ids not in (None, "", []):
        stmt = stmt.where(widget_master.c.sys_widget_id.in_(sys_widget_ids))
    if widget_type not in (None, ""):
        stmt = stmt.where(widget_master.c.widget_type == widget_type)
    if view_id not in (None, "", 0):
        stmt = stmt.where(widget_master.c.view_id == view_id)
    if widget_json not in (None, "", {}, []):
        stmt = stmt.where(widget_master.c.widget_json == widget_json)
    if created_by not in (None, "", 0):
        stmt = stmt.where(widget_master.c.created_by == created_by)
    if fetch_single == 1:
        return DB.executeDBSelectSingle(stmt)
    else:
        return DB.executeDBSelect(stmt)

def getWidgetCategoryDB():
    widget_master = DB.getTableMeta("sys_widgets_category").alias("wm")
    stmt = select(widget_master)
    stmt = stmt.where(
        widget_master.c.is_delete == 0
    )
    stmt = stmt.order_by(widget_master.c.sys_widget_cat_id.asc())
    return DB.executeDBSelect(stmt)

def insertUpdateWidget(widgetps):
    sys_widget_id = int(widgetps.sys_widget_id.get() or 0)
    sys_widget_cat_id = int(widgetps.sys_widget_cat_id.get() or 0)
    widget_type = widgetps.widget_type.get()
    widget_icon = widgetps.widget_icon.get()
    widget_title = widgetps.widget_title.get()
    widget_dtl = widgetps.widget_dtl.get()
    widget_json = widgetps.widget_json.get()
    view_id = int(widgetps.view_id.get() or 0)
    is_visible = int(widgetps.is_visible.get() or 0)
    is_multiple = int(widgetps.is_multiple.get() or 0)
    is_system = int(widgetps.is_system.get() or 0)
    is_global = int(widgetps.is_global.get() or 0)
    is_delete = int(widgetps.is_delete.get() or 0)
    created_by = int(userps.user_id.get() or 0)
    if widgetps.created_by.get() not in (None, "", 0):
        created_by = int(widgetps.created_by.get() or 0)
    values = {}
    if sys_widget_cat_id not in (None, "", 0):
        values["sys_widget_cat_id"] = sys_widget_cat_id
    if widget_type not in (None, ""):
        values["widget_type"] = widget_type
    if widget_icon not in (None, ""):
        values["widget_icon"] = widget_icon
    if widget_title not in (None, ""):
        values["widget_title"] = widget_title
    if widget_dtl not in (None, ""):
        values["widget_dtl"] = widget_dtl
    if widget_json not in (None, "", {}, []):
        values["widget_json"] = widget_json
    if view_id not in (None, "", 0):
        values["view_id"] = view_id
    if is_visible not in (None, ""):
        values["is_visible"] = is_visible
    if is_multiple not in (None, ""):
        values["is_multiple"] = is_multiple
    if is_system not in (None, ""):
        values["is_system"] = is_system
    if is_global not in (None, ""):
        values["is_global"] = is_global
    if is_delete not in (None, ""):
        values["is_delete"] = is_delete
    widget_master = DB.getTableMeta("sys_widget_master")
    if sys_widget_id not in (None, "", 0):
        stmt = update(widget_master).where(widget_master.c.sys_widget_id == sys_widget_id).values(**values)
        DB.executeDBUpdate(stmt)
    else:
        values["created_by"] = created_by
        values["created_date"] = nowWithTimeZone()
        stmt = insert(widget_master).values(**values)
        sys_widget_id = DB.executeDBInsert(stmt)
    return sys_widget_id

def insertUpdateUserWidget(widgetps):
    sys_widgets_users_id = int(widgetps.sys_widgets_users_id.get() or 0)
    sys_widget_id = int(widgetps.sys_widget_id.get() or 0)
    dashboard_id = int(widgetps.dashboard_id.get() or 0)
    user_id = int(widgetps.user_id.get() or 0)
    c_width = int(widgetps.c_width.get() or 0)
    c_height = int(widgetps.c_height.get() or 0)
    htm_flow = int(widgetps.htm_flow.get() or 0)
    bg_color = widgetps.bg_color.get()
    widget_label = widgetps.widget_label.get()
    widget_setting = widgetps.widget_setting.get()
    rank = int(widgetps.rank.get() or 0)
    values = {}
    if sys_widget_id not in (None, "", 0):
        values["sys_widget_id"] = sys_widget_id
    if dashboard_id not in (None, "", 0):
        values["dashboard_id"] = dashboard_id
    if user_id not in (None, "", 0):
        values["user_id"] = user_id
    if c_width not in (None, "", 0):
        values["c_width"] = c_width
    if c_height not in (None, "", 0):
        values["c_height"] = c_height
    if htm_flow not in (None, ""):
        values["htm_flow"] = htm_flow
    if bg_color not in (None, ""):
        values["bg_color"] = bg_color
    if widget_label not in (None, ""):
        values["widget_label"] = widget_label
    if widget_setting not in (None, "", {}, []):
        values["widget_setting"] = widget_setting
    if rank not in (None, ""):
        values["rank"] = rank
    sys_user_widgets = DB.getTableMeta("sys_user_widgets")
    if sys_widgets_users_id not in (None, "", 0):
        stmt = update(sys_user_widgets).where(sys_user_widgets.c.sys_widgets_users_id == sys_widgets_users_id).values(**values)
        DB.executeDBUpdate(stmt)
    else:
        values["created_by"] = userps.user_id.get()
        values["created_date"] = nowWithTimeZone()
        stmt = insert(sys_user_widgets).values(**values)
        sys_widgets_users_id = DB.executeDBInsert(stmt)
    return sys_widgets_users_id