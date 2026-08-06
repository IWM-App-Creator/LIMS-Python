from datetime import datetime
from app.utils.common import formatDate
from app.dbfunctions.systemviewfunctions import getSystemViewData

def getSystemView(systemviewps):
    view_dataarr = getSystemViewData(systemviewps)
    systemview_list = []
    for view in view_dataarr:
        row = {}
        for key, value in dict(view._mapping).items():
            if isinstance(value, datetime):
                row[key] = formatDate(value, "%Y-%m-%d %H:%M:%S")
            else:
                row[key] = value
        systemview_list.append(row)
    return systemview_list