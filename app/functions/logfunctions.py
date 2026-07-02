# # from jose import jwt, JWTError, ExpiredSignatureError
# from datetime import datetime, timedelta
# # from app.utils.config import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM

# def heresavelogfunction():
#     print("Log Here Properties Param : ")
#     # print("Log Here Properties Param : " + str(user_id) + " : " + email)


# def heresavelogfunction2():
#     print("Log Here Properties Param 2 : ")
#     # print("Log Here Properties Param : " + str(user_id) + " : " + email)


# # def heresavelogfunction(user_id: int, email: str):
# #     print("Log Here Properties Param : ")
# #     # print("Log Here Properties Param : " + str(user_id) + " : " + email)


from datetime import datetime
from sqlalchemy import insert, delete
# from app.config.database import db
from app.dbhelper.db_helper import DB

# from app.models.tables import sys_error_log

class ErrorLogFunctions:

    @staticmethod
    def save_error_log(
        view_id,
        log_type,
        section,
        desc,
        error_msg,
        user_id
    ):
        # users = getTableMeta("users", "systemconfig")
        # stmt = (
        #     select(users)
        #     .where(users.c.email == email)
        # )
        stmt = (
            insert(sys_error_log)
            .values(
                type=log_type,
                view_id = view_id,
                section = section,
                desc = desc,
                error_msg = error_msg,
                created_by = user_id,
                created_date = datetime.now()
            )
        )
        result = DB.executeDBInsert(stmt)
        return result
        # DB.commit()
        # return result.inserted_primary_key[0]

    @staticmethod
    def resolve_error(error_id):
        stmt = (
            delete(sys_error_log)
            .where(sys_error_log.c.error_id == error_id)
        )
        result = DB.execute(stmt)
        # DB.commit()
        return True