from sqlalchemy.orm import Session

def execute_stmt(engine, stmt, fetch="one"):

    with Session(engine) as db:

        result = db.execute(stmt).mappings()

        if fetch == "one":
            return result.first()

        elif fetch == "all":
            return result.all()

        return result