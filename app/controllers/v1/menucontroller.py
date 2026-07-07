from app.utils.common import select, DB, Request, RequestData, JSONResponse, raiseAPIError, userps
from app.dbfunctions.associationfunctions import getAssociationUsers
from app.dbfunctions.menufunctions import getDynamicMenuCenter, getUserMenuList
from app.properties.associationproperties import associationps
from app.properties.menuproperties import menups

def getUserSideMenu(request: Request):
    user_id = userps.user_id.get()
    menups.is_active.set(1)
    menups.created_by.set(user_id)
    menups.fetch_single.set(1)
    menucenter = getDynamicMenuCenter(menups)
    if menucenter and menucenter.m_centre_id not in (None, ""):
        menups.m_centre_id.set(menucenter.m_centre_id)
    else :
        associationps.user_id.set(user_id)
        associationps.fetch_single.set(1)
        association_mnu = getAssociationUsers(associationps)
        if association_mnu and association_mnu.defmenucntr not in (None, ""):
            menups.m_centre_id.set(association_mnu.defmenucntr)
            menups.usr_flag.set(1)
    menups.fetch_single.set(0)
    menus = getUserMenuList(menups)
    sidemenus = []
    for m in menus:
        row = {
            "menu_id": m.menu_id,
            "m_centre_id": m.m_centre_id,
            "parent_menu_id": m.parent_menu_id,
            "is_section": m.is_section,
            "menu_name": m.menu_name,
            "menu_url": m.menu_url,
            "menu_icon": m.menu_icon,
            "menu_color": m.menu_color,
            "m_type": m.m_type,
            "view_id": m.view_id,
            "is_new_tab": m.is_new_tab,
            "is_custom_centre": m.is_custom_centre,
            "rank": m.rank,
            "is_delete": m.is_delete,
            "created_by": m.created_by,
            "created_date": m.created_date.strftime("%Y-%m-%d %H:%M:%S"),
            "url": m.url,
            "view_url": m.view_url
        }
        sidemenus.append(row)
    return JSONResponse (
        status_code = 200,
        content = {
            "status": True,
            "message": "Menu Data",
            "sidemenus": sidemenus
        }
    )
