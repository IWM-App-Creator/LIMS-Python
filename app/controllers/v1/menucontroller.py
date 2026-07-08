from app.utils.common import select, DB, Request, RequestData, JSONResponse, raiseAPIError, raiseInvalidError, userps
from app.dbfunctions.associationfunctions import getAssociationUsers
from app.dbfunctions.menufunctions import getPublicOrUserMenuCenters, getDynamicMenu, getDynamicMenuCenter, getUserMenuList, insertUpdateUserMenu
from app.properties.associationproperties import associationps
from app.properties.menuproperties import menups
from app.functions.menuhelper import setMenuInputParam, setUserMenusOutput, setUserMenuCenterOutput
from app.dbfunctions.logfunctions import saveErrorLogtoDB

# --------------------------
# Menu Centre
# --------------------------
def getMenuCentre(request: Request):
    print("getMenuCentre --> ")
    asso_menu_cntr_ids = [8, 51, 60, 61] # Get User Menu Centre IDs From Association Users
    menups.m_centre_ids.set(asso_menu_cntr_ids)
    mymenus = getPublicOrUserMenuCenters(menups) # Get User Menu Centre and Public Menu Centre
    menups.menu_array.set(mymenus)
    setUserMenuCenterOutput(menups)
    return JSONResponse (
        status_code = 200,
        content = {
            "status": True,
            "message": "Menu Centre Data",
            "menu_centres": menups.menus_output.get()
        }
    )

def saveMenuCentre(request: Request):
    print("saveMenuCentre")

def setMenuCentreActive(request: Request):
    print("setMenuCentreActive")

def resetMenuCentre(request: Request):
    print("resetMenuCentre")

def copyMenuCentre(request: Request):
    print("copyMenuCentre")

# --------------------------
# Menu
# --------------------------
def getUserMenu(request: Request):
    try:
        params = RequestData.params(request)
        menups.m_centre_id.set(params.get("m_centre_id", ""))
        if menups.m_centre_id.get() in (None, "", 0):
            return raiseInvalidError("Menu Center is not found", 404)
        menu_array = getUserMenuList(menups)
        menups.menu_array.set(menu_array)
        setUserMenusOutput(menups)
        return JSONResponse (
            status_code = 200,
            content = {
                "status": True,
                "message": "Menu Data",
                "menu_data": menups.menus_output.get()
            }
        )
    except Exception as e:
        raiseAPIError(str(e), 500)

def saveUserMenu(request: Request):
    try:
        menu_id = ""
        status = True
        params = RequestData.params(request)
        menups.callfrom.set(params.get("callfrom", ""))
        menups.view_id.set(params.get("view_id", 0))
        is_valid = 1
        if menups.callfrom.get() == "ViewPage": # Call From User View Page
            menups.is_active.set(1)
            menups.created_by.set(userps.user_id.get())
            menups.fetch_single.set(1)
            menups.is_delete.set(0)
            menu_center = getDynamicMenuCenter(menups)
            if menu_center and menu_center.m_centre_id not in (None, "", 0):
                menups.m_centre_id.set(menu_center.m_centre_id)
            menups.is_delete.set(None)
            menups.m_type.set(1)
            user_menu = getDynamicMenu(menups)
            if user_menu:
                menu_id = user_menu.menu_id
                if user_menu.is_delete == 1:
                    menups.menu_id.set(user_menu.menu_id)
                    menups.m_type.set(0)
                    menups.is_delete.set(0)
                    menups.m_centre_id.set(None)
                    menups.created_by.set(None)
                    menups.view_id.set(None)
                    menups.is_new_tab.set(None)
                    menups.is_custom_centre.set(None)
                    menups.rank.set(None)
                    insertUpdateUserMenu(menups)
                    is_valid = 2
                else :
                    is_valid = 0
        if is_valid == 1:
            menups.fetch_single.set(1)
            menups.order_by.set("rank")
            menups.order_type.set("desc")
            menups.created_by.set(userps.user_id.get())
            menups.view_id.set(None)
            menups.m_centre_id.set(None)
            menups.m_type.set(0)
            user_menu = getDynamicMenu(menups)
            if user_menu:
                menups.rank.set(user_menu.rank + 1)
            setMenuInputParam(menups, params)
            menups.is_delete.set(0)
            menups.parent_menu_id.set(0)
            menu_id = insertUpdateUserMenu(menups)
            if menups.add_custom_view.get() == 1:
                menups.menu_id.set(menu_id)
            status = True
        elif is_valid == 2:
            status = True
        else :
            status = False
        return JSONResponse (
            status_code = 200,
            content = {
                "status": status,
                "message": "Menu Saved Successfully",
                "menu_id": menu_id
            }
        )
    except Exception as e:
        saveErrorLogtoDB("SaveMenu", 0, "saveUserMenu", str(e)) # Log Error To DB
        raiseAPIError(str(e), 500)

def updateUserMenu(request: Request):
    print("updateUserMenu")

def saveMenuSorting(request: Request):
    print("saveMenuSorting")

def removeUserMenu(request: Request):
    print("removeUserMenu")

def getMenuIcons(request: Request):
    print("getMenuIcons")



    # public function saveUserMenu(Request $request) {
    #     $menu_id = "";
    #     $fetch_flag = 0;
    #     $output_array = array();
    #     /* Input Params */
    #     $user_id = empty(Input::get('user_id')) ? "1" : Input::get('user_id');
    #     $api_secret = empty(Input::get('api_secret')) ? "" : Input::get('api_secret');
    #     $m_centre_id = empty(Input::get('m_centre_id')) ? "0" : Input::get('m_centre_id');
    #     $m_type = empty(Input::get('m_type')) ? "1" : Input::get('m_type');
    #     $view_id = empty(Input::get('view_id')) ? "0" : Input::get('view_id');
    #     $menu_name = empty(Input::get('menu_name')) ? "" : Input::get('menu_name');
    #     $menu_icon = empty(Input::get('menu_icon')) ? "" : Input::get('menu_icon');
    #     $menu_color = empty(Input::get('menu_color')) ? "" : Input::get('menu_color');
    #     $menu_url = empty(Input::get('menu_url')) ? "" : Input::get('menu_url');
    #     $is_new_tab = empty(Input::get('is_new_tab')) ? "0" : Input::get('is_new_tab');
    #     $add_custom_view = empty(Input::get('add_custom_view')) ? "0" : Input::get('add_custom_view');
    #     $is_section = empty(Input::get('is_section')) ? "0" : Input::get('is_section');
    #     $callfrom = empty(Input::get('callfrom')) ? "" : Input::get('callfrom');
    #     /* API Check */
    #     $ModelFunctionsController = new ModelFunctionsController();
    #     $userdtlarr = $ModelFunctionsController->getAPIUserHeader($user_id, $api_secret, 1);
    #     if($userdtlarr) {
    #         $is_valid = 1;
    #         if($callfrom == "ViewPage") { /* Called From View */
    #             $menuc = DB::table('sys_dynamic_menu_centre')
    #                         ->where('is_active', 1)
    #                         ->where('is_delete', 0)
    #                         ->where('created_by', $user_id)
    #                         ->first();
    #             if($menuc) {
    #                 $m_centre_id = $menuc->m_centre_id;
    #             }
    #             $menu = DB::table('sys_dynamic_menu')
    #                     ->where('m_type', 1)
    #                     ->where('m_centre_id', $m_centre_id)
    #                     ->where('view_id', $view_id)
    #                     ->where('created_by', $user_id)
    #                     ->first();
    #             if($menu) {
    #                 $menu_id = $menu->menu_id;
    #                 if($menu->is_delete == 1) {
    #                     $data = array();
    #                     $data['is_delete'] = 0;
    #                     DB::table('sys_dynamic_menu')->where('menu_id', $menu_id)->update($data);
    #                     $is_valid = 2;    
    #                 } else {
    #                     $is_valid = 0;
    #                 }
    #             }
    #         }
    #         if($is_valid == 1) {
    #             $rank = 0;
    #             $menu = DB::table('sys_dynamic_menu')
    #                     ->where('created_by', $user_id)
    #                     ->where('is_delete', '0')
    #                     ->orderBy('rank', 'DESC')
    #                     ->first();
    #             if($menu) {
    #                 $rank = (int)$menu->rank + 1;
    #             }
    #             $data = array();
    #             $data['parent_menu_id'] = '0';
    #             $data['m_centre_id'] = $m_centre_id;
    #             $data['is_section'] = $is_section;
    #             $data['menu_name'] = $menu_name;
    #             $data['menu_url'] = $menu_url;
    #             $data['menu_icon'] = $menu_icon;
    #             $data['menu_color'] = $menu_color;
    #             $data['m_type'] = $m_type;
    #             $data['view_id'] = $view_id;
    #             $data['is_new_tab'] = $is_new_tab;
    #             $data['rank'] = $rank;
    #             $data['is_delete'] = "0";
    #             $data['created_by'] = $user_id;
    #             $data['created_date'] = date('Y-m-d H:i:s');
    #             $menu_id = DB::table('sys_dynamic_menu')->insertGetId($data);
    #             if($add_custom_view == '1') {
    #                 $this->saveCustomView($menu_id, $menu_name, $menu_url, $user_id);
    #             }
    #             $fetch_flag = 1;
    #         } else if($is_valid == 2) {
    #             $fetch_flag = 1;
    #         } else {
    #             $fetch_flag = 2;
    #         }
    #     }
    #     $output_array['fetch_flag'] = $fetch_flag;
    #     $output_array['menu_id'] = $menu_id;
    #     echo json_encode($output_array);
    # }
