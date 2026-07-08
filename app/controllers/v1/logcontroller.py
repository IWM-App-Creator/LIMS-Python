from app.utils.common import Request, RequestData, raiseAPIError
from app.services.firebase.firebase_service import send_push
from app.dbfunctions.logfunctions import getErrorLog, saveErrorLog, resolveError

# http://xytovet.localhost:8000/api/v1//log/geterrors?view_id=178
def getErrorLog(request: Request):
    try:
        params = RequestData.params(request)
        viewhlp.setViewInputParam(viewps, params) # Get Input Param Data
        getErrorLog() # Get View Data
        if not viewps.userview.get(): # Invalid View
            return raiseInvalidError("View Not Found", 401)
        
        
        viewhlp.setViewOutputArray(viewps); # Output Json
        return JSONResponse (
            status_code = 200,
            content = {
                "status": True,
                "message": "View Data",
                "view_data": viewps.output_array.get()
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
