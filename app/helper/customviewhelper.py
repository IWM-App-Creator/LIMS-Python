from app.dbfunctions.customviewfunctions import getCustomViewData

def getCustomViewList(customvwps):
    customview_list = getCustomViewData(customvwps)
    customviews = []
    for view in customview_list:
        row = {
            "custom_view_id": view.custom_view_id,
            "view_name": view.view_name,
            "view_url": view.view_url,
            "dync_cat_id": view.dync_cat_id,
            "short_desc": view.short_desc,
            "preview_img": view.preview_img,
        }
        customviews.append(row)
    return customviews