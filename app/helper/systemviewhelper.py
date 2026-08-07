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
        for colalias in colarray:
            parts = colalias.split("-")
            colnm = parts[0]
            colalias = parts[1]
            value = data.get(colnm) # Get DB Data
            if isinstance(value, datetime):
                value = formatDate(value)
            row[colalias] = value  # Set DB Data
        systemview_list.append(row)
    return systemview_list