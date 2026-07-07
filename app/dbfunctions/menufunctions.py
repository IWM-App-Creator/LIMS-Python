from app.utils.common import select, DB, JSONResponse, raiseAPIError, userps

def getMenuCentre():
    # m_centre_id = userps.user_id.get() # Get User ID
    # Prepare Query
    tblmcentre = DB.getTableMeta("sys_dynamic_menu_centre").alias("sdmc")
    stmt = select(tblmcentre).where(tblmcentre.c.is_delete == 0)
    # if m_centre_id not in (None, ""):
    #     stmt = stmt.where(tblmcentre.c.id == m_centre_id)
    return DB.executeDBSelectSingle(stmt)

    # $menuc = DB::table('sys_dynamic_menu_centre')->where('m_centre_id', $m_center_id)->first();
    #                     if($menuc) {
    #                         $centre_name = $menuc->centre_name;
    #                         $data = array();
    #                         $data['centre_name'] = $centre_name;
    #                         $data['ref_m_c_id'] = $m_center_id;
    #                         $data['is_public'] = 0;
    #                         $data['is_active'] = 0;
    #                         $data['created_by'] = $user_id;
    #                         $data['created_date'] = date('Y-m-d H:i:s');
    #                         $new_m_centre_id = DB::table('sys_dynamic_menu_centre')->insertGetId($data);
    #                         $this->copyMenuList($m_center_id, $new_m_centre_id, $user_id, $userdtlarr);
    #                         $m_centre_id = $new_m_centre_id;
    #                     }

def getMenuFromMenuCentre():
    print(getMenuFromMenuCentre)

def getUserMenuList(user_id):
    m_centre_id = 0
    usr_flag = 0
    # ---------------------------------------
    # Check user's active menu centre
    # ---------------------------------------
    sys_dynamic_menu_centre = DB.getTableMeta("sys_dynamic_menu_centre").alias("sdmc")
    stmt = (
        select(sys_dynamic_menu_centre)
        .where(sys_dynamic_menu_centre.c.is_active == 1)
        .where(sys_dynamic_menu_centre.c.is_delete == 0)
        .where(sys_dynamic_menu_centre.c.created_by == user_id)
    )
    m_centre_id = DB.getSingleColumnValue(stmt, "m_centre_id", 0)
    if m_centre_id in (None, "", 0):
        # ---------------------------------------
        # Get default menu centre from association
        # ---------------------------------------
        sys_association_users = DB.getTableMeta("sys_association_users").alias("sau")
        stmt = (
            select(sys_association_users.c.defmenucntr)
            .where(sys_association_users.c.user_id == user_id)
            .where(sys_association_users.c.is_delete == 0)
            .order_by(sys_association_users.c.srno.asc())
        )
        m_centre_id = DB.getSingleColumnValue(stmt, "defmenucntr", 0)
        if m_centre_id in (None, "", 0):
            usr_flag = 1
    # ---------------------------------------
    # Get side menus
    # ---------------------------------------
    sys_dynamic_menu = DB.getTableMeta("sys_dynamic_menu").alias("sdm")
    sys_dynamic_view = DB.getTableMeta("sys_dynamic_view").alias("sdv")
    sys_custom_view = DB.getTableMeta("sys_custom_view").alias("scv")
    stmt = (
        select(
            sys_dynamic_menu,
            sys_dynamic_view.c.url,
            sys_custom_view.c.view_url
        )
        .select_from(
            sys_dynamic_menu
            .outerjoin(
                sys_dynamic_view,
                sys_dynamic_view.c.view_id == sys_dynamic_menu.c.view_id
            )
            .outerjoin(
                sys_custom_view,
                sys_custom_view.c.custom_view_id == sys_dynamic_menu.c.view_id
            )
        )
        .where(sys_dynamic_menu.c.m_centre_id == m_centre_id)
        .where(sys_dynamic_menu.c.is_delete == 0)
    )
    if usr_flag == 0:
        stmt = stmt.where(sys_dynamic_menu.c.created_by == user_id)
    stmt = stmt.order_by(sys_dynamic_menu.c.rank.asc())
    sidemenus = DB.executeDBSelect(stmt)
    print("sidemenus --> ", sidemenus)
    return sidemenus