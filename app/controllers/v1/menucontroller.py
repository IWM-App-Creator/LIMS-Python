from app.utils.common import select, DB, Request, RequestData, JSONResponse, raiseAPIError, raiseInvalidError, userps
from app.dbfunctions.logfunctions import saveErrorLogtoDB
from app.dbfunctions.menufunctions import insertUpdateMenuCentre
from app.helper.generalfunctions import normalizeJson
from app.properties.menuproperties import menups

def saveMenuCentre(request: Request):
    print("saveMenuCentre --> ")
    try:
        params = request.params
        menups.m_centre_id.set(params.get("m_centre_id", 0))
        menups.centre_name.set(params.get("centre_name", ""))
        menups.ref_m_c_id.set(params.get("ref_m_c_id", 0))
        menups.menu_json.set(normalizeJson(params.get("menu_json", []), []))
        menups.short_desc.set(params.get("short_desc", ""))
        menups.is_public.set(params.get("is_public", 0))
        menups.is_active.set(params.get("is_active", 0))
        menups.is_delete.set(params.get("is_delete", 0))
        insertUpdateMenuCentre(menups)
    except Exception as e:
        saveErrorLogtoDB("Menu", menups.view_id.get(), "saveMenuCentre", str(e)) # Log Error To DB
        raiseAPIError(str(e), 500)