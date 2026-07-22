import json
from app.utils.common import select, DB, userps
from app.dbfunctions.dbtablesfunctions import getDBTableData
from app.dbfunctions.viewlayoutfunctions import getViewLayoutDataByID
from app.helper.generalfunctions import sortObjectsByKey
from app.properties.dbproperties import dbps
from app.helper import dbhelper as dbhlp

def setViewLayoutParam(viewps, params):
    viewps.view_id.set(params.get("view_id", ""))
    # viewps.call_from.set(params.get("call_from", "DynamicView"))
    # viewps.tab_id.set(params.get("tab_id", "0"))
    # viewps.page_no.set(params.get("page_no", 1))
    # viewps.search_text.set(params.get("search_text", ""))
    # viewps.filterqry.set(params.get("filterqry", ""))
