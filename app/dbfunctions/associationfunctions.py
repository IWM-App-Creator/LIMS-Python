from app.utils.common import DB, select, func, text, userps, or_

def getAssociationData(associationps):
    schema_name = associationps.schema_name.get()
    association = DB.getTableMeta("sys_associations", schema_name).alias("a")
    association_users = DB.getTableMeta("sys_association_users", schema_name).alias("au")
    db_tables = DB.getTableMeta("sys_db_tables", schema_name).alias("dbt")
    db_tbl_cols = DB.getTableMeta("sys_db_tables_cols", schema_name).alias("dbtc")
    lkup_tbl_cols = DB.getTableMeta("sys_db_tables_cols", schema_name).alias("lkuptc")
    stmt = (
        select(
            association,
            db_tables.c.table_name,
            db_tables.c.table_alias,
            db_tbl_cols.c.col_name,
            db_tbl_cols.c.col_alias,
            lkup_tbl_cols.c.col_name.label("lookup_col_name"),
            lkup_tbl_cols.c.col_alias.label("lookup_col_alias"),
        )
        .distinct()
        .outerjoin(
            db_tables,
            association.c.table_id == db_tables.c.table_id,
        )
        .outerjoin(
            db_tbl_cols,
            association.c.col_id == db_tbl_cols.c.col_id,
        )
        .outerjoin(
            lkup_tbl_cols,
            association.c.lookup_col_id == lkup_tbl_cols.c.col_id,
        )
        .where(association.c.is_delete == 0)
    )
    if int(userps.role_id.get()) != 1 and int(userps.ws_role_id.get()) != 1:
        stmt = (
            stmt.outerjoin(
                association_users,
                association.c.associations_id == association_users.c.associations_id,
            )
            .where(
                association_users.c.user_id == userps.user_id.get(),
            )
        )
    stmt = stmt.order_by(association.c.name.asc())
    return DB.executeDBSelect(stmt)

def getAssociationDesignationData(associationps):
    schema_name = associationps.schema_name.get()
    assoc_designation = DB.getTableMeta("sys_assoc_designation", schema_name).alias("ad")
    designation = DB.getTableMeta("sys_designation", schema_name).alias("d")
    stmt = (
        select(
            assoc_designation,
            designation.c.designation_name
        )
        .outerjoin(
            designation,
            assoc_designation.c.designation_id == designation.c.designation_id,
        )
        .where(assoc_designation.c.is_delete == 0)
        .where(assoc_designation.c.associations_id == associationps.associations_id.get())
        .order_by(assoc_designation.c.srno.asc())
    )
    return DB.executeDBSelect(stmt)

def getAssociationLookupData(associationps):
    schema_name = associationps.schema_name.get()
    pgno = int(associationps.pgno.get())
    lookup_table = DB.getTableMeta(associationps.table_name.get(), schema_name).alias("lt")
    association_users = DB.getTableMeta("sys_association_users", schema_name).alias("au")
    pcol = lookup_table.c[associationps.pcol_nm.get()]
    lcol = lookup_table.c[associationps.lcol_nm.get()]
    stmt = (
        select(
            pcol.label("value"),
            lcol.label("label")
        )
        .distinct()
        .where(
            lookup_table.c.is_delete == 0,
            lcol.is_not(None)
        )
    )
    if associationps.txtsearch.get():
        stmt = stmt.where(
            lcol.like(f"%{associationps.txtsearch.get()}%")
        )
    if (int(userps.role_id.get()) != 1 and int(userps.ws_role_id.get()) != 1):
        subquery = (
            select(association_users.c.col_p_val)
            .where(
                association_users.c.user_id == userps.user_id.get(),
                association_users.c.col_id == associationps.pcol_id.get(),
                association_users.c.is_delete == 0,
            )
        )
        stmt = stmt.where(
            pcol.in_(subquery)
        )
    record_qry = select(func.count()).select_from(stmt.subquery())
    associationps.record_cnt.set(DB.executeDBScalar(record_qry))
    mainstmt = (
        stmt.order_by(
            pcol.desc(),
            lcol.asc()
        )
        .offset((pgno - 1) * 10)
        .limit(10)
    )
    return DB.executeDBSelect(mainstmt)

def getAssociationUsersByDesignation(associationps):
    schema_name = associationps.schema_name.get()
    values = associationps.col_p_vals.get()
    association_users = DB.getTableMeta("sys_association_users", schema_name).alias("au")
    stmt = (
        select(
            association_users.c.col_p_val,
            func.group_concat(association_users.c.user_id).label("user_ids"),
            association_users.c.designation_id,
            func.max(association_users.c.is_owner).label("is_owner"),
            func.max(association_users.c.is_edit).label("is_edit"),
            func.max(association_users.c.is_view).label("is_view"),
            func.max(association_users.c.is_noaccess).label("is_noaccess"),
            func.max(association_users.c.is_notify).label("is_notify"),
            func.max(association_users.c.dyncviews).label("dyncviews"),
            func.max(association_users.c.custlink).label("custlink"),
            func.max(association_users.c.menucntr).label("menucntr"),
            func.max(association_users.c.defmenucntr).label("defmenucntr"),
            func.max(association_users.c.modules).label("modules"),
            func.max(association_users.c.dashboardcntr).label("dashboardcntr"),
            func.max(association_users.c.defdashboard).label("defdashboard"),
        )
        .where(
            association_users.c.col_id == associationps.pcol_id.get(),
            association_users.c.col_p_val.in_(values),
            association_users.c.is_delete == 0,
        )
        .group_by(
            association_users.c.col_p_val,
            association_users.c.designation_id,
        )
    )
    return DB.executeDBSelect(stmt)

def getDesignationData(associationps):
    schema_name = associationps.schema_name.get()
    designation = DB.getTableMeta("sys_designation", schema_name).alias("d")
    stmt = select(designation)
    if associationps.designation_id.get() not in (None, "", 0):
        stmt = stmt.where(designation.c.designation_id == associationps.designation_id.get())
    stmt = stmt.where(designation.c.is_delete == 0)
    if associationps.fetch_single.get() == 1:
        return DB.executeDBSelectSingle(stmt)
    else :
        return DB.executeDBSelect(stmt)    

def getAssociationUsers(associationps):
    view_id = int(associationps.view_id.get() or 0)
    col_p_val = int(associationps.col_p_val.get() or 0)
    associations_id = int(associationps.associations_id.get() or 0)
    designation_id = int(associationps.designation_id.get() or 0)
    user_id = int(associationps.user_id.get() or 0)
    col_id = int(associationps.col_id.get() or 0)
    is_notify = int(associationps.is_notify.get() or 0)
    assousers = DB.getTableMeta("sys_association_users").alias("au")
    stmt = select(assousers)
    if associations_id not in (None, "", 0):
        stmt = stmt.where(assousers.c.associations_id == associations_id)
    if designation_id not in (None, "", 0):
        stmt = stmt.where(assousers.c.designation_id == designation_id)
    if associationps.user_id.get() not in (None, "", 0):
        stmt = stmt.where(assousers.c.user_id == user_id)
    if associationps.col_id.get() not in (None, "", 0):
        stmt = stmt.where(assousers.c.col_id == col_id)
    if col_p_val not in (None, "", 0):
        stmt = stmt.where(assousers.c.col_p_val == col_p_val)
    if is_notify not in (None, ""):
        stmt = stmt.where(assousers.c.is_notify == is_notify)
    if view_id not in (None, "", 0):
        stmt = stmt.where(
            func.find_in_set(
                view_id,
                func.json_unquote(
                    func.json_extract(
                        assousers.c.access_json,
                        "$.dyncviews",
                    )
                ),
            )
            > 0,
        )
    stmt = stmt.where(assousers.c.is_delete == 0)
    stmt = stmt.order_by(assousers.c.srno.asc())
    if associationps.is_distinct.get() == 1:
        stmt = stmt.distinct()
    if associationps.fetch_single.get() == 1:
        associationps.ass_users_data.set(DB.executeDBSelectSingle(stmt))
    else :
        associationps.ass_users_data.set(DB.executeDBSelect(stmt))

def getAssociationViews(associationps):
    assoviews = DB.getTableMeta("sys_association_view").alias("av")
    stmt = select(assoviews)
    if associationps.view_id.get() not in (None, "", 0):
        stmt = stmt.where(assoviews.c.view_id == int(associationps.view_id.get()))
    view_ids = associationps.view_ids.get()
    if view_ids not in (None, "", 0):
        view_id_list = [int(x) for x in view_ids.split(",") if x.strip()]
        stmt = stmt.where(assoviews.c.view_id.in_(view_id_list))
    stmt = stmt.where(assoviews.c.is_delete == 0)
    if associationps.fetch_single.get() == 1:
        return DB.executeDBSelectSingle(stmt)
    else :
        return DB.executeDBSelect(stmt)

def getAssociationDesignation(associationps):
    asso_designation = DB.getTableMeta("sys_assoc_designation").alias("ad")
    stmt = select(asso_designation)
    if associationps.associations_id.get() not in (None, "", 0):
        stmt = stmt.where(asso_designation.c.associations_id == associationps.associations_id.get())
    if associationps.designation_id.get() not in (None, "", 0):
        stmt = stmt.where(asso_designation.c.designation_id == associationps.designation_id.get())
    stmt = stmt.where(asso_designation.c.is_delete == 0)
    if associationps.fetch_single.get() == 1:
        return DB.executeDBSelectSingle(stmt)
    else :
        return DB.executeDBSelect(stmt)

def getViewAssociationByUser(associationps):
    user_id = associationps.user_id.get()
    view_id = associationps.view_id.get()
    association_users = DB.getTableMeta("sys_association_users").alias("sa_user")
    associations = DB.getTableMeta("sys_associations").alias("sa")
    designation = DB.getTableMeta("sys_designation").alias("sd")
    stmt = ( 
        select(association_users, designation.c.designation_name, associations.c.name, associations.c.full_access)
        .outerjoin(
            associations,
            association_users.c.associations_id == associations.c.associations_id,
        )
        .outerjoin(
            designation,
            association_users.c.designation_id == designation.c.designation_id,
        )
        .where(
            association_users.c.user_id == user_id,
            association_users.c.is_delete == 0,
            func.find_in_set(
                view_id,
                func.json_unquote(
                    func.json_extract(
                        association_users.c.access_json,
                        "$.dyncviews",
                    )
                ),
            )
            > 0,
        )
        .order_by(association_users.c.col_p_val.asc())
    )
    # print("stmt --> ", stmt)
    return DB.executeDBSelect(stmt)

from collections import defaultdict

def getAssociationsForNotification(associationps):
    association_users = DB.getTableMeta("sys_association_users")
    associations = DB.getTableMeta("sys_associations")
    table = DB.getTableMeta("sys_db_tables").alias("tbl")
    tablecols = DB.getTableMeta("sys_db_tables_cols").alias("cols")
    lkptablecols = DB.getTableMeta("sys_db_tables_cols").alias("lkpcols")
    is_admin = userps.role_id.get() == 1 or userps.ws_role_id.get() == 1
    stmt = (
        select(
            association_users.c.col_p_val,
            associations.c.table_id,
            table.c.table_name,
            tablecols.c.col_name,
            lkptablecols.c.col_name.label("lookup_col_name"),
        )
        .outerjoin(
            associations,
            association_users.c.associations_id == associations.c.associations_id,
        )
        .outerjoin(table, table.c.table_id == associations.c.table_id)
        .outerjoin(tablecols, tablecols.c.col_id == associations.c.col_id)
        .outerjoin(lkptablecols, lkptablecols.c.col_id == associations.c.lookup_col_id)
        .where(
            association_users.c.is_notify == 1,
            association_users.c.is_delete == 0,
            func.find_in_set(
                associationps.view_id.get(),
                func.json_unquote(
                    func.json_extract(
                        association_users.c.access_json,
                        "$.dyncviews",
                    )
                ),
            )
            > 0,
        )
    )
    if not is_admin:
        stmt = stmt.where(
            or_(
                association_users.c.user_id == associationps.user_id.get(),
                associations.c.inter_msg == 1,
            )
        )

    rows = DB.executeDBSelect(stmt.distinct())

    if not rows:
        return []

    # Group by dynamic table/columns
    groups = defaultdict(list)

    for row in rows:
        key = (row.table_name, row.col_name, row.lookup_col_name)
        groups[key].append(row.col_p_val)

    result = []

    for (tbl_name, pcol_name, lcol_name), values in groups.items():

        tbl = DB.getTableMeta(tbl_name).alias("t")

        pcol = tbl.c[pcol_name]
        lcol = tbl.c[lcol_name]

        q = (
            select(
                pcol.label("value"),
                lcol.label("label"),
            )
            .where(
                tbl.c.is_delete == 0,
                pcol.in_(values),
            )
            .distinct()
        )
        result.extend({"value": r.value, "label": str(r.label),} for r in DB.executeDBSelect(q))
    if result is not []:
        result.sort(key=lambda x: (x["label"] or "").lower())
    return result