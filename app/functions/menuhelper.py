import json
from app.utils.common import userps
from app.properties.associationproperties import associationps
from app.dbfunctions.associationfunctions import getAssociationUsers
from app.dbfunctions.menufunctions import getDynamicMenuCenter

def resetMenuProperties(menups):
    menups.m_centre_id.set(None)
    menups.menu_id.set(None)
    menups.parent_menu_id.set(None)
    menups.m_type.set(None)
    menups.view_id.set(None)
    menups.menu_name.set(None)
    menups.menu_icon.set(None)
    menups.menu_color.set(None)
    menups.menu_url.set(None)
    menups.is_new_tab.set(None)
    menups.is_custom_centre.set(None)
    menups.add_custom_view.set(None)
    menups.rank.set(None)
    menups.is_section.set(None)
    menups.callfrom.set(None)
    menups.is_delete.set(None)

def setMenuInputParam(menups, params):
    menups.menu_id.set(params.get("menu_id", None))
    menups.m_centre_id.set(params.get("m_centre_id", None))
    menups.m_type.set(params.get("m_type", None))
    menups.view_id.set(params.get("view_id", None))
    menups.menu_name.set(params.get("menu_name", None))
    menups.menu_icon.set(params.get("menu_icon", None))
    menups.menu_color.set(params.get("menu_color", None))
    menups.menu_url.set(params.get("menu_url", None))
    menups.is_new_tab.set(params.get("is_new_tab", None))
    menups.add_custom_view.set(params.get("add_custom_view", None))
    menups.is_section.set(params.get("is_section", None))

def getActiveMenuCenterID(menups):
    # menups.usr_flag.set(0)
    # menups.is_active.set(1)
    menups.created_by.set(userps.user_id.get())
    # menups.fetch_single.set(1)
    if menups.menu_exe_data.get() is None :
        getDynamicMenuCenter(menups)

    menucenter = menups.menu_exe_data.get()
    if menucenter and menucenter.m_centre_id not in (None, "", 0):
        menups.m_centre_id.set(menucenter.m_centre_id)
    else :
        associationps.user_id.set(userps.user_id.get())
        associationps.fetch_single.set(1)
        association_mnu = getAssociationUsers(associationps)
        if association_mnu and association_mnu.defmenucntr not in (None, ""):
            menups.m_centre_id.set(association_mnu.defmenucntr)
            menups.usr_flag.set(1)

def setUserMenusOutput(menups):
    menu_array = menups.menu_array.get()
    sidemenus = []
    for m in menu_array:
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
            "url": m.url,
            "view_url": m.view_url
        }
        sidemenus.append(row)
    menups.menus_output.set(sidemenus)

def setUserMenuCenterOutput(menups):
    menu_array = menups.menu_array.get()
    sidemenus = []
    for m in menu_array:
        row = {
            "m_centre_id": m.m_centre_id,
            "centre_name": m.centre_name,
            "ref_m_c_id": m.ref_m_c_id,
            "short_desc": m.short_desc,
            "preview_img": m.preview_img,
            "dync_cat_id": m.dync_cat_id,
            "is_public": m.is_public,
            "is_active": m.is_active,
        }
        sidemenus.append(row)
    menups.menus_output.set(sidemenus)