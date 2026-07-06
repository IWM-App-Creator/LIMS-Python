from sqlalchemy import select
from app.utils.common import DB, JSONResponse, raiseAPIError, userps
from app.functions.userfunctions import getUserDataFromDB


def getUserDetail(): # token: str
    print("getUserDetail:", userps.user_id.get())
    # --------------------------
    # Get User Data
    # --------------------------
    # tbluser = DB.getTableMeta("users", "systemconfig").alias("usr")
    # stmt = (
    #     select(tbluser).where(tbluser.c.id == userps.user_id.get())
    # )
    # user = DB.executeDBSelectSingle(stmt)
    # if not user: # Invalid User
    #     raiseAPIError("Invalid User ID", 401)

    user = getUserDataFromDB() # Execute Function to User Get Data
    userps.first_name.set(user.first_name)
    userps.last_name.set(user.last_name)
    userps.email.set(user.email)
    userps.user_settings.set(user.user_settings)
    user_dict = {
        "user_id": userps.user_id.get(),
        "role_id": userps.role_id.get(),
        "first_name": userps.first_name.get(),
        "last_name": userps.last_name.get(),
        "email": userps.email.get(),
        "user_settings": userps.user_settings.get(),
    }
    # --------------------------
    # Get User Menu
    # --------------------------
    user_menu = {
        "m_centre_id": userps.user_id.get(),
        "role_id": userps.role_id.get(),
        "first_name": userps.first_name.get(),
        "last_name": userps.last_name.get(),
        "email": userps.email.get(),
    }
    # --------------------------
    # Merge All Data & Send Response
    # --------------------------
    return JSONResponse (
        status_code = 200,
        content = {
            "status": True,
            "message": "User Data",
            "user_dict": user_dict,
            "user_menu": user_menu,
        }
    )
    # return JSONResponse (
    #     status_code = 200,
    #     content = {
    #         "status": True,
    #         "message": "Login successful",
    #         
    #         "role_id": userps.role_id.get(),
    #         "ws_role_id": userps.ws_role_id.get(),
    #         "workspace_id": userps.workspace_id.get(),
    #         "workspace_name": userps.workspace_name.get(),
    #         "ws_url": userps.ws_url.get()
    #     }
    # )

def getUserList():
    print("getUserList:")
