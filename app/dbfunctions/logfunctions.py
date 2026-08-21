from app.utils.common import DB, select, insert, delete, func, userps, nowWithTimeZone, globalps
import traceback
import sys

def getDBErrorLog(logps):
    page_no = logps.page_no.get()
    error_id = logps.error_id.get()
    section = logps.section.get()
    item_id = logps.item_id.get()
    page_size = logps.page_size.get()
    page_no = max(1, int(page_no))
    offset = (page_no - 1) * page_size
    tblerrorlog = DB.getTableMeta("sys_error_log").alias("errlog")
    tbluser = DB.getTableMeta("users", "systemconfig").alias("usr")
    tblview = DB.getTableMeta("sys_new_dynamic_view").alias("dyncv")
    stmt = (
        select(tblerrorlog, tbluser.c.first_name, tbluser.c.last_name, tblview.c.view_name, tblview.c.url)
        .select_from(
            tblerrorlog
            .outerjoin(
                tbluser,
                tblerrorlog.c.created_by == tbluser.c.id
            )
            .outerjoin(
                tblview,
                (tblerrorlog.c.section == "View") &
                (tblerrorlog.c.item_id == tblview.c.view_id)
            )
        )
    )
    if section not in (None, "", 0):
        stmt = stmt.where(tblerrorlog.c.section == section)
    if item_id not in (None, "", 0):
        stmt = stmt.where(tblerrorlog.c.item_id == item_id)
    if error_id not in (None, "", 0):
        stmt = stmt.where(tblerrorlog.c.error_id == error_id)
    # Create count statement from the existing statement
    count_stmt = stmt.with_only_columns(func.count()).order_by(None)
    logps.total_record.set(DB.executeDBScalar(count_stmt))
    # Apply paging to the original statement
    stmt = (
        stmt.order_by(tblerrorlog.c.created_date.desc())
            .limit(page_size)
            .offset(offset)
    )
    logdata = DB.executeDBSelect(stmt)
    logps.logdata.set(logdata)

def getDBErrorLogCount(logps):
    tblerrorlog = DB.getTableMeta("sys_error_log").alias("errlog")
    stmt = (
        select(func.count())
        .select_from(tblerrorlog)
    )
    total_unread = DB.executeDBScalar(stmt)
    logps.error_count.set(total_unread)

def saveErrorLogtoDB(section: str, item_id: str, notes: str, error_msg: str, page_url: str = ""):
    error_id = 0
    try:
        if item_id == "" :
            item_id = "0"
        # For Local Development : Log Bug In Console    
        if globalps.DB_DEBUG_LEVEL == "Print" :
            tb = sys.exc_info()[2]
            if tb is not None:
                last_tb = traceback.extract_tb(tb)[-1]
                notes = f"{notes} :- {last_tb.filename} : ({last_tb.name} - {last_tb.lineno}"
            print("Exception DB_DEBUG_LEVEL Print --> ", notes)
        # Log Bug To Database
        if globalps.DB_DEBUG_LEVEL == "DB":
            sys_error_log = DB.getTableMeta("sys_error_log")
            stmt = (
                insert(sys_error_log)
                .values(
                    section = section,
                    item_id = item_id,
                    notes = notes,
                    page_url = page_url,
                    error_msg = error_msg,
                    created_by = userps.user_id.get(),
                    created_date = nowWithTimeZone()
                )
            )
            error_id = DB.executeDBInsert(stmt)
        
    except Exception as e:
        print(f"Error while saving error log: {str(e)}")
    return error_id

def resolveError(error_id: str):
    sys_error_log = DB.getTableMeta("sys_error_log")
    stmt = ( delete(sys_error_log).where(sys_error_log.c.error_id == error_id) )
    DB.executeDBDelete(stmt)