from app.utils.common import select, DB, Request, RequestData, JSONResponse, raiseAPIError, userps
from app.dbfunctions.associationfunctions import getAssociationUsers
from app.dbfunctions.menufunctions import getDynamicMenuCenter, getUserMenuList
from app.properties.associationproperties import associationps
from app.properties.menuproperties import menups
from app.functions.menuhelper import getMenuCenterId, setUserMenusOutput

def getUserMenu(request: Request):
    try:
        params = RequestData.params(request)
        menups.m_centre_id.set(params.get("m_centre_id", ""))
        menu_array = getUserMenuList(menups)
        menups.menu_array.set(menu_array)
        setUserMenusOutput(menups)
        return JSONResponse (
            status_code = 200,
            content = {
                "status": True,
                "message": "Menu Data",
                "view_data": menups.menus_output.get()
            }
        )
    except Exception as e:
        raiseAPIError(str(e), 500)