from app.utils.common import DB, select, or_, func, case, userps

def getWSListByUsers(wsps):
    userid = userps.user_id.get()
    if wsps.ws_usr_id.get() > 0 :
        userid = wsps.ws_usr_id.get()
    ws_srch = wsps.ws_srch.get()

    tblworkspace = DB.getTableMeta("workspace_master", "systemconfig").alias("ws")
    tblwsuser = DB.getTableMeta("users_workspace", "systemconfig").alias("wsusr")
    tbluser = DB.getTableMeta("users", "systemconfig").alias("usr")
    role_count_sq = (
        select(
            tblwsuser.c.workspace_id,
            func.sum(case((tblwsuser.c.ws_role_id == 1, 1), else_=0)).label("ownercnt"),
            func.sum(case((tblwsuser.c.ws_role_id == 2, 1), else_=0)).label("usercnt"),
            func.sum(case((tblwsuser.c.ws_role_id.not_in([1, 2]), 1), else_=0)).label("noaccesscnt"),
        )
        .select_from(
            tblwsuser.join(
                tbluser,
                tbluser.c.id == tblwsuser.c.user_id
            )
        )
        .where(tbluser.c.is_delete == 0)
        .where(tblwsuser.c.is_delete == 0)
        .group_by(tblwsuser.c.workspace_id)
    ).subquery("rolecnt")
    stmt = (
        select(
            tblworkspace,
            tblwsuser.c.ws_role_id,
            role_count_sq.c.ownercnt,
            role_count_sq.c.usercnt,
            role_count_sq.c.noaccesscnt,
        )
        .select_from(
            tblworkspace
            .join(
                tblwsuser,
                tblworkspace.c.workspace_id == tblwsuser.c.workspace_id
            )
            .join(
                tbluser,
                tbluser.c.id == tblwsuser.c.user_id
            )
            .outerjoin(
                role_count_sq,
                role_count_sq.c.workspace_id == tblworkspace.c.workspace_id
            )
        )
        .where(tbluser.c.id == userid)
        .where(tblworkspace.c.workspace_id > 1)
        .where(tblworkspace.c.is_delete == 0)
        .where(tblwsuser.c.is_delete == 0)
        .where(tbluser.c.is_delete == 0)
    )
    if ws_srch:
        stmt = stmt.where(
            or_(
                tblworkspace.c.workspace_name.like(f"%{ws_srch}%"),
                tblworkspace.c.schema_name.like(f"%{ws_srch}%")
            )
        )
    stmt = stmt.order_by(tblworkspace.c.workspace_id.desc())
    ws_data = DB.executeDBSelect(stmt)
    wsps.ws_data.set(ws_data)

def getUserWSData(wsps):
    userid = userps.user_id.get()
    if wsps.ws_usr_id.get() > 0 :
        userid = wsps.ws_usr_id.get()
    workspace_master = DB.getTableMeta("workspace_master", "systemconfig").alias("ws")
    users_workspace = DB.getTableMeta("users_workspace", "systemconfig").alias("wsusr")
    stmt = (
        select(
            workspace_master.c.workspace_id,
            workspace_master.c.workspace_name,
            workspace_master.c.ws_url,
            workspace_master.c.schema_name,
            users_workspace.c.ws_role_id,
            users_workspace.c.is_accepted
        )
        .join(
            users_workspace,
            users_workspace.c.workspace_id == workspace_master.c.workspace_id,
        )
        .where(workspace_master.c.is_delete == 0)
        .where(users_workspace.c.ws_role_id < 3)
        .where(users_workspace.c.is_delete == 0)
        .where(users_workspace.c.user_id == userid)
    )
    if wsps.domain_flag.get() == 1:
        stmt = stmt.where(workspace_master.c.ws_url == userps.req_subdomain.get())
    if wsps.fetch_single.get() == 1:
        wsps.ws_data.set(DB.executeDBSelectSingle(stmt))
    else:
        wsps.ws_data.set(DB.executeDBSelect(stmt))

def getWorkspaceActiveURL():
    workspace_master = DB.getTableMeta("workspace_master", "systemconfig").alias("ws")
    stmt = (
        select(workspace_master.c.ws_url)
        .where(workspace_master.c.workspace_id == userps.workspace_id.get())
        .limit(1)
    )
    return DB.getSingleColumnValue(stmt, "ws_url", "")

def isWorkspaceValid(subdomain: str):
    ws_url = subdomain
    if subdomain == "" :
        ws_url = userps.ws_url.get()
    workspace_master = DB.getTableMeta("workspace_master", "systemconfig").alias("ws")
    stmt = (
        select(workspace_master.c.workspace_id)
        .where(workspace_master.c.ws_url == ws_url)
        .limit(1)
    )
    return DB.getSingleColumnValue(stmt, "workspace_id", "0")