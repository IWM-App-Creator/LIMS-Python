from app.utils.common import select, DB, JSONResponse, raiseAPIError, userps

def getMenuCentre():
    # m_centre_id = userps.user_id.get() # Get User ID
    # Prepare Query
    tblmcentre = DB.tableMeta("sys_dynamic_menu_centre").alias("sdmc")
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