from sqlalchemy import text
from sqlalchemy.orm import Session
from app.database.database import engine


def execute_query(query, params=None, fetch="one"):

    with Session(engine) as db:

        result = db.execute(
            text(query),
            params or {}
        ).mappings()

        if fetch == "one":
            return result.first()

        elif fetch == "all":
            return result.all()

        return result