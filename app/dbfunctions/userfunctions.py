from app.utils.common import select, DB, userps

def getUserDataFromDB():
    user_id = userps.user_id.get() # Get User ID
    email = userps.email.get() # Get User Email
    # Prepare Query
    tbluser = DB.getTableMeta("users", "systemconfig").alias("usr")
    stmt = select(tbluser)
    if user_id not in (None, ""):
        stmt = stmt.where(tbluser.c.id == user_id)
    if email not in (None, ""):
        stmt = stmt.where(tbluser.c.email == email)
    user = DB.executeDBSelectSingle(stmt) # Execute Query
    return user


def getUserDataByID(user_id):
    tbluser = DB.getTableMeta("users", "systemconfig").alias("usr")
    stmt = select(tbluser).where(tbluser.c.id == user_id)
    user = DB.executeDBSelectSingle(stmt) # Execute Query
    return user

# id, role_id, first_name, last_name, email, phone, password, user_settings, company_name, profile_pic, user_sign, remember_token, usr_pwd, api_secret, public_key, refresh_token, xero_token, auto_login, active_ws, reset_pass_key, reset_pwd_datetime, ws_activation_key, status, is_darkmode, is_delete, time_zone, created_by, is_metadata, created_at, updated_at