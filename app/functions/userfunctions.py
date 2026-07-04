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