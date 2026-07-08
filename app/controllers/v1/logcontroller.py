from app.utils.common import Request, RequestData, JSONResponse, raiseAPIError, formatDate
from app.services.firebase.firebase_service import send_push
from app.dbfunctions.logfunctions import getDBErrorLog, saveErrorLogtoDB, resolveError
from app.functions.generalfunctions import formatUserDisplayName

# http://xytovet.localhost:8000/api/v1//log/geterrors?error_id=&section=View&item_id=178
def getErrorLog(error_id: str, section: str, item_id: str):
    try:
        logdata = getDBErrorLog(error_id, section, item_id) # Get Error Log Data
        item_list = []
        if not logdata: # Invalid View
            return raiseAPIError("Log Not Found", 401)
        for data in logdata:
            first_name = getattr(data, "first_name", "")
            last_name = getattr(data, "last_name", "")
            user_name = formatUserDisplayName(first_name = first_name, last_nam = last_name)
            item = {
                "error_id": getattr(data, "error_id", "0"),
                "section": getattr(data, "section", ""),
                "item_id": getattr(data, "item_id", "0"),
                "notes": getattr(data, "notes", ""),
                "error_msg": getattr(data, "error_msg", ""),
                "user_name": user_name,
                "view_name": getattr(data, "view_name", ""),
                "url": getattr(data, "url", ""),
                "created_date": formatDate(created_date = getattr(data, "created_date", "")),
            }
            item_list.append(item)
        return JSONResponse (
            status_code = 200,
            content = {
                "status": True,
                "message": "Error Log Data",
                "log_data": item_list
            }
        )
    except Exception as e:
        raiseAPIError(str(e), 500)

# def saveLog(token: str):
#     print(f"Token received: {token}")
    # result = verify_token(token)
    # return result

# http://xytovet.localhost:8000/api/v1//log/saveerror?view_id=178
async def saveErrorLog(request: Request):
    # request.state.params
    # print("saveLog --> ")
    # print("IS_LOCAL_DEV --> ", globalps.IS_LOCAL_DEV)
    # print("saveLog user_id --> ", globalps.user_id)
    # print("saveLog workspace_id --> ", globalps.workspace_id)
    # print("saveLog workspace_name --> ", globalps.workspace_name)
    # print("saveLog ws_url --> ", globalps.ws_url)
    # print("saveLog schema_name --> ", userps.schema_name.get())
    params = RequestData.params(request)
    # print("request -->", params)
    print("request -->", params["view_id"])
    # sys_dynamic_view = DB.getTableMeta("sys_dynamic_view").alias("sdv")
    # stmt = (
    #     select(sys_dynamic_view)
    #         .where(sys_dynamic_view.c.is_delete == 0)
    # )
    # # print("stmt --> ", stmt)
    # row = DB.executeDBSelectSingle(stmt)
    # print("row --> ", row)
    # view_id = params.get("view_id")
    # user_id = params.get("user_id")
    # print("saveLog view_id -->", view_id)
    # print("saveLog user_id -->", user_id)

# http://xytovet.localhost:8000/api/v1//log/removeerror?view_id=178
def removeErrorLog(request: Request):
    print("saveLog user_id -->")

def testFireBasePush(token: str):
    response = send_push (
        token = token,
        title = "Test Notification",
        body = "Hello from Python"
    )
    return { "firebase_response": response }
