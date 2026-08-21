from app.utils.common import DB, select, insert, update, func, case, literal, exists, String, and_, or_, nowWithTimeZone, userps

def getWidgetsDB(widgetps):
    dashboard_id = int(widgetps.dashboard_id.get() or 0)
    sys_widget_cat_id = int(widgetps.sys_widget_cat_id.get() or 0)
    search_text = widgetps.search_text.get()
    widget_type = widgetps.widget_type.get()
    view_id = int(widgetps.view_id.get() or 0)
    page_size = 12
    pg_no = int(widgetps.pg_no.get() or 1)
    tbl_widget = DB.getTableMeta("sys_widget_master").alias("wm")
    tbl_view = DB.getTableMeta("sys_new_dynamic_view").alias("dv")
    user_dashboard = DB.getTableMeta("sys_user_dashboard").alias("dash")
    # ---------------------------------------------------------
    # Check whether widget is already added to dashboard
    # ---------------------------------------------------------
    widget_exists = exists(
        select(1).where(
            and_(
                user_dashboard.c.dashboard_id == dashboard_id,
                func.json_search(
                    user_dashboard.c.widget_list,
                    "one",
                    func.cast(
                        tbl_widget.c.sys_widget_id,
                        String
                    ),
                    None,
                    "$[*].sys_widget_id"
                ).isnot(None)
            )
        )
    )
    # ---------------------------------------------------------
    # Main query
    # ---------------------------------------------------------
    stmt = (
        select(
            tbl_widget,
            tbl_view.c.view_name,
            tbl_view.c.url
        )
        .outerjoin(
            tbl_view,
            tbl_view.c.view_id == tbl_widget.c.view_id
        )
    )
    # ---------------------------------------------------------
    # Filters
    # ---------------------------------------------------------
    if sys_widget_cat_id:
        stmt = stmt.where(
            tbl_widget.c.sys_widget_cat_id == sys_widget_cat_id
        )
    if search_text:
        stmt = stmt.where(
            tbl_widget.c.widget_title.like(f"%{search_text}%")
        )
    if widget_type:
        stmt = stmt.where(
            tbl_widget.c.widget_type == widget_type
        )
    if view_id:
        stmt = stmt.where(
            tbl_widget.c.view_id == view_id
        )
    # ---------------------------------------------------------
    # Role restriction
    # ---------------------------------------------------------
    if userps.role_id.get() != 1 and userps.ws_role_id.get() != 1:
        stmt = stmt.where(
            tbl_widget.c.widget_type.notin_(
                ["ADDUSER", "ADDVIEW"]
            )
        )
    # ---------------------------------------------------------
    # Created/system/global widgets
    # ---------------------------------------------------------
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
    # ---------------------------------------------------------
    # Don't show already-added widgets.
    #
    # is_multiple = 1 -> always show
    # is_multiple != 1 -> hide if already added
    # ---------------------------------------------------------
    stmt = stmt.where(
        or_(
            tbl_widget.c.is_multiple == 1,
            ~widget_exists
        )
    )
    # ---------------------------------------------------------
    # Order
    # ---------------------------------------------------------
    stmt = stmt.order_by(
        tbl_widget.c.is_system.desc(),
        tbl_widget.c.sys_widget_id.asc()
    )
    # ---------------------------------------------------------
    # Count AFTER filtering already-added widgets
    # ---------------------------------------------------------
    count_stmt = stmt.with_only_columns(
        func.count()
    ).order_by(None)
    total_count = DB.executeDBScalar(count_stmt)
    widgetps.rcrd_cnt.set(total_count)
    # ---------------------------------------------------------
    # Pagination
    # ---------------------------------------------------------
    offset = (pg_no - 1) * page_size
    stmt = (
        stmt
        .offset(offset)
        .limit(page_size)
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
    if widgetps.upd_vals.get() not in (None, "", {}):
        values = widgetps.upd_vals.get()
    else:
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