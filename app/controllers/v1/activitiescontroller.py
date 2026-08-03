from app.utils.common import Request, RequestData, JSONResponse, raiseAPIError
from app.helper.datetime import formatDate
from app.helper.generalfunctions import formatUserDisplayName
from app.dbfunctions.logfunctions import saveErrorLogtoDB
from app.dbfunctions.activitiesfunctions import getActivityLogs, getActivityLogById
from app.properties.activitiesproperties import activitiesps

def getActivities(request: Request):
    try:
        params = RequestData.params(request)
        # set params to Properties
        activitiesps.tableids.set(params.get("tableids", None))
        activitiesps.data_id.set(params.get("data_id", None))
        activitiesps.item_id.set(params.get("item_id", None))
        activitiesps.logtype.set(params.get("logtype", ""))
        activitiesps.viewflag.set(params.get("viewflag", 0))
        activitylogarr = getActivityLogs(activitiesps)
        activitylogs = []
        for actlog in activitylogarr:
            first_name = ""
            last_name = ""
            updatedby = (actlog.updatedby or "").split("**")
            if len(updatedby) == 2:
                first_name = updatedby[0].strip()
                last_name = updatedby[1].strip()
            row = {
                "log_id": actlog.log_id,
                "data_id": actlog.data_id,
                "table_id": actlog.table_id,
                "item_id": actlog.item_id,
                "col_id": actlog.col_id,
                "col_name": actlog.col_name,
                "col_alias": actlog.col_alias,
                "old_value": actlog.old_value,
                "new_value": actlog.new_value,
                "desc": actlog.desc,
                "is_notify": actlog.is_notify,
                "updated_by": actlog.updated_by,
                "updated_name": (formatUserDisplayName(first_name, last_name, "INITIAL") or ""),
                "u_fullname": (actlog.updatedby or "").replace("**", " "),
                "updated_date": formatDate(actlog.updated_date, "%d/%m/%y"),
                "u_datetime": formatDate(actlog.updated_date, "%d/%m/%y %H:%M:%S")
            }
            if activitiesps.viewflag.get() in (1, "1"):
                row["view_name"] = actlog.view_name
            activitylogs.append(row)
        return JSONResponse(
            status_code = 200,
            content = {
                "status": True,
                "message": "Activity Log List",
                "activitylogs": activitylogs
            }
        )
    except Exception as e:
        saveErrorLogtoDB("Activities", activitiesps.data_id.get(), "getActivities", str(e))
        raiseAPIError(str(e), 500)

def revertActivities(request: Request):
    print("revertActivities --> ")
    try:
        params = RequestData.params(request)
        activitiesps.log_id.set(params.get("log_id", 0))
        log_data = getActivityLogById(activitiesps)
        print("log_data --> ", log_data)
    except Exception as e:
        saveErrorLogtoDB("Activities", activitiesps.data_id.get(), "revertActivities", str(e))
        raiseAPIError(str(e), 500)