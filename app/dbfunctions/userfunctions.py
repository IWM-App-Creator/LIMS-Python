from app.utils.common import select, DB, userps, update, insert

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

def insertUpdateUserData():
    tbluser = DB.getTableMeta("users", "systemconfig")
    user_id = userps.user_id.get() # Get User ID
    if userps.othr_userid.get() not in (None, "", 0):
        user_id = userps.othr_userid.get()
    values = {}
    if userps.db_upd_vals.get() not in (None, {}, ""):
        values = userps.db_upd_vals.get()
    else:
        if userps.role_id.get() not in (None, "", 0):
            values["role_id"] = userps.role_id.get()
        if userps.first_name.get() not in (None, ""):
            values["first_name"] = userps.first_name.get()
        if userps.last_name.get() not in (None, ""):
            values["last_name"] = userps.last_name.get()
        if userps.email.get() not in (None, ""):
            values["email"] = userps.email.get()
        if userps.phone.get() not in (None, ""):
            values["phone"] = userps.phone.get()
        if userps.password.get() not in (None, ""):
            values["password"] = userps.password.get()
        if userps.user_settings.get() not in (None, {}):
            values["user_settings"] = userps.user_settings.get()
    if user_id not in (None, "", 0):
        stmt = (
            update(tbluser)
            .where(tbluser.c.id == user_id)
            .values(**values)
        )
        DB.executeDBUpdate(stmt)
    else:
        stmt = (
            insert(tbluser)
            .values(**values)
        )
        user_id = DB.executeDBInsert(stmt)
    return user_id

# id, role_id, first_name, last_name, email, phone, password, user_settings, remember_token, usr_pwd, api_secret, refresh_token, xero_token, auto_login, reset_pass_key, reset_pwd_datetime, ws_activation_key, status, is_delete, created_by, is_metadata, created_at, updated_at

# {"active_ws": 6, "pg_layout": "", "time_zone": "Australia/Perth", "user_sign": "", "public_key": "ZmlOeMPT1eI74sLAVzejHe52SPr2ND", "is_darkmode": 0, "profile_pic": "", "theme_color": "", "company_name": "Xytovet"}