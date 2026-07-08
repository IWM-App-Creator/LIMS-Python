from app.utils.common import Request, RequestData, JSONResponse, raiseAPIError, formatDate
from app.services.firebase.firebase_service import send_push
from app.dbfunctions.logfunctions import getDBErrorLog, saveErrorLogtoDB, resolveError
from app.functions.generalfunctions import formatUserDisplayName

# http://tesetws1.localhost:8000/api/v1/log/geterrors?error_id=&section=View&item_id=178
def getErrorLog(error_id: str, section: str, item_id: str):
    try:
        logdata = getDBErrorLog(error_id, section, item_id) # Get Error Log Data
        item_list = []
        if not logdata: # Invalid View
            return raiseAPIError("Log Not Found", 401)
        for data in logdata:
            first_name = getattr(data, "first_name", "")
            last_name = getattr(data, "last_name", "")
            user_name = formatUserDisplayName(first_name = first_name, last_name = last_name)
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

# http://tesetws1.localhost:8000/api/v1//log/saveerror?section=View&item_id=178&notes=notes&error_msg=test error message
async def saveErrorLog(section: str, item_id: str, notes: str, error_msg: str):
    try:
        error_id = saveErrorLogtoDB(section, item_id, notes, error_msg)
        return JSONResponse (
            status_code = 200,
            content = {
                "status": True,
                "message": "Error Log Saved Successfully",
                "error_id": error_id
            }
        )
    except Exception as e:
        raiseAPIError(str(e), 500)

# http://tesetws1.localhost:8000/api/v1/log/removeerror?view_id=178
def removeErrorLog(error_id: str):
    try:
        resolveError(error_id)
        return JSONResponse (
            status_code = 200,
            content = {
                "status": True,
                "message": "Error Log Removed Successfully",
                "error_id": error_id
            }
        )
    except Exception as e:
        raiseAPIError(str(e), 500)

def testFireBasePush(token: str):
    response = send_push (
        token = token,
        title = "Test Notification",
        body = "Hello from Python"
    )
    return { "firebase_response": response }
