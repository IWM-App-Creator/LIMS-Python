from sqlalchemy.orm import Session
from app.database.database import dbconn

# To Execute Statement (Query Builder)
def execute_stmt(stmt, fetch="one"):
    with Session(dbconn) as db:
        result = db.execute(stmt).mappings()
        if fetch == "one":
            return result.first()
        elif fetch == "all":
            return result.all()
        return result