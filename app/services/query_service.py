from sqlalchemy import text

def execute_query(db, query, params=None):

    result = db.execute(
        text(query),
        params or {}
    )

    return result.mappings().first()
    # return result.mappings().all()