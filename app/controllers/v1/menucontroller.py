from app.utils.common import select, DB, Request, RequestData, JSONResponse, raiseAPIError, raiseInvalidError, userps
from app.dbfunctions.logfunctions import saveErrorLogtoDB
from app.dbfunctions.menufunctions import getMenuCentreData, insertUpdateMenuCentre
from app.helper.generalfunctions import normalizeJson
from app.properties.menuproperties import menups

def getMenuCentre(request: Request):
    print("getMenuCentre")
    try:
        asso_menu_cntr_ids = [] # Get User Menu Centre IDs From Association Users
        menups.m_centre_ids.set(asso_menu_cntr_ids)
        menups.created_by.set(userps.user_id.get())
        menu_centres = getMenuCentreData(menups)
        menu_centre = []
        for menu in menu_centres:
            menu_json = menu.menu_json
            if isinstance(menu_json, str):
                menu_json = eval(menu_json)
            if not isinstance(menu_json, list):
                menu_json = []
            row = {
                "m_centre_id": menu.m_centre_id,
                "centre_name": menu.centre_name,
                "menu_json": menu_json,
                "short_desc": menu.short_desc,
                "preview_img": menu.preview_img,
                "is_public": menu.is_public,
                "is_active": menu.is_active,
                "created_by": menu.created_by
            }
            menu_centre.append(row)
        return JSONResponse (
            status_code = 200,
            content = {
                "status": True,
                "message": "Menu Centre Data",
                "menu_centres": menu_centre
            }
        )
    except Exception as e:
        # saveErrorLogtoDB ("Menu", 0, "getMenuCentre", str(e)) # Log Error To DB
        raiseAPIError(str(e), 500)

def saveMenuCentre(request: Request):
    print("saveMenuCentre --> ")
    try:
        params = RequestData.params(request)
        menups.m_centre_id.set(params.get("m_centre_id", 0))
        menups.centre_name.set(params.get("centre_name", ""))
        menups.ref_m_c_id.set(params.get("ref_m_c_id", 0))
        menups.menu_json.set(normalizeJson(params.get("menu_json", []), []))
        menups.short_desc.set(params.get("short_desc", ""))
        menups.is_public.set(params.get("is_public", 0))
        menups.is_active.set(params.get("is_active", 0))
        menups.is_delete.set(params.get("is_delete", 0))
        insertUpdateMenuCentre(menups)
        return JSONResponse (
            status_code = 200,
            content = {
                "status": True,
                "message": "Menu Centre Saved Successfully",
                "m_centre_id": menups.m_centre_id.get()
            }
        )
    except Exception as e:
        saveErrorLogtoDB("Menu", 0, "saveMenuCentre", str(e)) # Log Error To DB
        raiseAPIError(str(e), 500)