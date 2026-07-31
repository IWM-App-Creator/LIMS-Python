from app.dbfunctions.filterfunctions import getViewFiltersDB

def getSaveFilters(filterps):
    filterarr = getViewFiltersDB(filterps)
    filter_list = []
    for flt in filterarr:
        row = {
            "save_id": getattr(flt, "save_id", 0),
            "save_name": getattr(flt, "save_name", ""),
            "view_id": getattr(flt, "view_id", 0),
            "view_qry_json": getattr(flt, "view_qry_json", []),
            "is_default": getattr(flt, "is_default", 0),
            "widget_added": getattr(flt, "widget_added", 0)
        }
        filter_list.append(row)
    return filter_list