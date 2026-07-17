from app.utils.common import DB, select, func, text, userps, or_

def getAssociationData(associationps):
    association = DB.getTableMeta("sys_associations").alias("a")
    stmt = select(association)
    if associationps.association_id.get() not in (None, "", 0):
        stmt = stmt.where(association.c.associations_id == associationps.association_id.get())
    stmt = stmt.where(association.c.is_delete == 0)
    return stmt

def getDesignationData(associationps):
    designation = DB.getTableMeta("sys_designation").alias("d")
    stmt = select(designation)
    if associationps.designation_id.get() not in (None, "", 0):
        stmt = stmt.where(designation.c.designation_id == associationps.designation_id.get())
    stmt = stmt.where(designation.c.is_delete == 0)
    if associationps.fetch_single.get() == 1:
        return DB.executeDBSelectSingle(stmt)
    else :
        return DB.executeDBSelect(stmt)

def getAssociationUsers(associationps):
    assousers = DB.getTableMeta("sys_association_users").alias("au")
    stmt = select(assousers)
    if associationps.associations_id.get() not in (None, "", 0):
        stmt = stmt.where(assousers.c.associations_id == associationps.associations_id.get())
    if associationps.designation_id.get() not in (None, "", 0):
        stmt = stmt.where(assousers.c.designation_id == associationps.designation_id.get())
    if associationps.user_id.get() not in (None, "", 0):
        stmt = stmt.where(assousers.c.user_id == associationps.user_id.get())
    if associationps.col_id.get() not in (None, "", 0):
        stmt = stmt.where(assousers.c.col_id == associationps.col_id.get())
    if associationps.col_p_val.get() not in (None, "", 0):
        stmt = stmt.where(assousers.c.col_p_val == associationps.col_p_val.get())
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
        stmt = stmt.where(assoviews.c.view_id == associationps.view_id.get())
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
            text(f"FIND_IN_SET('{view_id}', dyncviews)")
        )
        .order_by(association_users.c.col_p_val.asc())
    )
    # print("stmt --> ", stmt)
    return DB.executeDBSelect(stmt)

def getAssociationsForNotification(associationps):
    association_users = DB.getTableMeta("sys_association_users")
    associations = DB.getTableMeta("sys_associations")
    is_admin = 0
    if userps.role_id.get() == 1 or userps.ws_role_id.get() == 1:
        is_admin = 1
    stmt = (
        select(
            association_users.c.col_id,
            association_users.c.col_p_val,
            associations.c.lookup_col_id
        )
        .select_from(
            association_users
            .outerjoin(
                associations,
                association_users.c.associations_id == associations.c.associations_id
            )
        )
        .where(association_users.c.is_notify == 1)
        .where(association_users.c.is_delete == 0)
    )
    stmt = stmt.where(
        func.find_in_set(
            associationps.view_id.get(),
            func.json_unquote(
                func.json_extract(association_users.c.access_json, "$.dyncviews")
            )
        ) > 0
    )
    if is_admin == 0:
        stmt = stmt.where(
            or_(
                association_users.c.user_id == associationps.user_id.get(),
                associations.c.inter_msg == 1
            )
        )
    stmt = stmt.distinct()
    assousers = DB.executeDBSelect(stmt)
    asso_notify = []
    for usr in assousers:
        row = {
            "col_id": usr.col_id,
            "lookup_col_id": usr.lookup_col_id,
            "col_p_val": usr.col_p_val
        }
        asso_notify.append(row)
    return asso_notify

#   public function checkViewAssociation($dvps) {
#         $dvps->full_access = 0;
#         $dvps->prmqry = "";
#         $asso_tbl = "mltb";
#         $asso_col = "";
#         $assocol_ids = array();
#         // $GeneralFunctions = new GeneralFunctions();
#         // DB::enableQueryLog();
#         $dvps->assousers = DB::table('sys_association_users')
#                                 ->select('sys_association_users.*', 'sys_designation.designation_name', 'sys_associations.name', 'sys_associations.full_access')
#                                 ->leftjoin('sys_associations', 'sys_association_users.associations_id', '=', 'sys_associations.associations_id')
#                                 ->leftjoin('sys_designation', 'sys_association_users.designation_id', '=', 'sys_designation.designation_id')
#                                 ->whereRaw("FIND_IN_SET('" . $dvps->view_id . "', dyncviews)")
#                                 ->where('sys_association_users.user_id', $dvps->user_id)
#                                 ->where('sys_association_users.is_delete', '0')
#                                 ->orderBy('col_p_val', 'ASC') 
#                                 ->get();
#         // $query_array = DB::getQueryLog();
#         // $GeneralFunctions->displayQuery($query_array);
#         // exit;
#         foreach($dvps->assousers as $assousr) {
#             if($assousr->full_access == 1) {
#                 $dvps->full_access = 1;
#                 if($dvps->fa_is_owner == 0 &&  $assousr->is_owner > 0) {
#                     $dvps->fa_asso_id = $assousr->associations_id;
#                     $dvps->fa_dsgn_id = $assousr->designation_id;
#                     $dvps->fa_dsgn_nm = $assousr->designation_name;
#                     $dvps->fa_is_owner = $assousr->is_owner;
#                     $dvps->fa_is_edit = "1"; //$assousr->is_edit;
#                     $dvps->fa_is_view = "1"; // $assousr->is_view;
#                     $dvps->fa_is_noaccess = "1"; // $assousr->is_noaccess;
#                 } else if($dvps->fa_is_edit == 0 &&  $assousr->is_edit > 0) {
#                     $dvps->fa_asso_id = $assousr->associations_id;
#                     $dvps->fa_dsgn_id = $assousr->designation_id;
#                     $dvps->fa_dsgn_nm = $assousr->designation_name;
#                     $dvps->fa_is_owner = $assousr->is_owner;
#                     $dvps->fa_is_edit = $assousr->is_edit;
#                     $dvps->fa_is_view = "1"; //$assousr->is_view;
#                     $dvps->fa_is_noaccess = "1"; //$assousr->is_noaccess;
#                 } else if($dvps->fa_is_view == 0 &&  $assousr->is_view > 0) {
#                     $dvps->fa_asso_id = $assousr->associations_id;
#                     $dvps->fa_dsgn_id = $assousr->designation_id;
#                     $dvps->fa_dsgn_nm = $assousr->designation_name;
#                     $dvps->fa_is_owner = $assousr->is_owner;
#                     $dvps->fa_is_edit = $assousr->is_edit;
#                     $dvps->fa_is_view = $assousr->is_view;
#                     $dvps->fa_is_noaccess = "1"; //$assousr->is_noaccess;
#                 } else if($dvps->fa_is_noaccess == 0 &&  $assousr->is_noaccess > 0) {
#                     $dvps->fa_asso_id = $assousr->associations_id;
#                     $dvps->fa_dsgn_id = $assousr->designation_id;
#                     $dvps->fa_dsgn_nm = $assousr->designation_name;
#                     $dvps->fa_is_owner = $assousr->is_owner;
#                     $dvps->fa_is_edit = $assousr->is_edit;
#                     $dvps->fa_is_view = $assousr->is_view;
#                     $dvps->fa_is_noaccess = $assousr->is_noaccess;
#                 }
#             }
#             array_push($assocol_ids, $assousr->col_p_val);
#         }
#         if($dvps->full_access == 0) {
#             foreach($dvps->assousers as $assousr) {
#                 if(!$asso_col) {
#                     /* Get Table Column Name */
#                     foreach($dvps->viewcols as $viewcol) {
#                         if($assousr->col_id == $viewcol->col_id) {
#                             $asso_tbl = $viewcol->table_name;
#                             $asso_col = $viewcol->col_name;
#                         }
#                     }
#                 }
#             }
#             $dvps->prmqry = $asso_tbl . "." . $asso_col . " In (" . implode(",", $assocol_ids) . ")";
#         }
#     }
