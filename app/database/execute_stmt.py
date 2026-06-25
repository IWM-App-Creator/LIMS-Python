from sqlalchemy.orm import Session
from app.database.database import engine


def execute_stmt(stmt, fetch="one"):

    with Session(engine) as db:

        result = db.execute(stmt).mappings()

        if fetch == "one":
            return result.first()

        elif fetch == "all":
            return result.all()

        return result