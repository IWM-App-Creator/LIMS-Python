from datetime import datetime
from app.utils.common import formatDate
from app.dbfunctions.systemviewfunctions import getSystemViewData

def getSystemView(systemviewps):
    view_dataarr = getSystemViewData(systemviewps)
    colarray = systemviewps.colarray.get()
    systemview_list = []
    for view in view_dataarr:
        data = dict(view._mapping)   # Convert Row to dict
        row = {}
        for col in colarray:
            value = data.get(col)
            if isinstance(value, datetime):
                value = formatDate(value)
            row[col] = value
        systemview_list.append(row)
    return systemview_list