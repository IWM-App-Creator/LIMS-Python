import json
from app.utils.common import userps
from app.dbfunctions.menufunctions import getMenuCentreData

def getUserMenuList(menups):
    menups.created_by.set(userps.user_id.get())
    menups.m_centre_id.set(None)
    menups.is_active.set(None)
    menups.is_public.set(None)
    menus = getMenuCentreData(menups)
    menu_list = []
    for menu in menus:
        row = {
            "m_centre_id": menu.m_centre_id,
            "centre_name": menu.centre_name,
            "menu_json": menu.menu_json,
            "short_desc": menu.short_desc,
            "preview_img": menu.preview_img,
            "is_public": menu.is_public,
            "is_active": menu.is_active,
            "created_by": menu.created_by
        }
        menu_list.append(row)
    menups.menu_cntr_data.set(menu_list)
