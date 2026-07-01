from sqlalchemy import text
from sqlalchemy.orm import Session
from app.database.database import dbconn

# To Execute Direct SQL Query
# e.g. 
# qry = """
    # SELECT 
    #     users.*
    # FROM users
    # WHERE users.email = :email
    # """
    # user = execute_query(qry,{"email": email}, "one")


def execute_query(query, params = None, fetch = "one"):
    with Session(dbconn) as db:
        result = db.execute(
            text(query),
            params or {}
        ).mappings()
        if fetch == "one":
            return result.first()
        elif fetch == "all":
            return result.all()
        return result