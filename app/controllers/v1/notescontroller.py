from app.utils.common import Request, RequestData, JSONResponse, getTimeAgoValue
from app.helper.datetime import formatDate
from app.helper.generalfunctions import formatUserDisplayName
from app.dbfunctions.notesfunctions import getNotes
from app.properties.notesproperties import notesps

def getUserNotes(request: Request):
    print("getUserNotes --> ")
    params = RequestData.params(request)
    notesps.view_id.set(params.get("view_id", 0))
    notesps.item_id.set(params.get("item_id", 0))
    notesps.showdel.set(params.get("showdel", 0))
    notesarr = getNotes(notesps)
    user_notes = []
    for note in notesarr:
        row = {
            "notes_id": note.notes_id,
            "parent_id": note.parent_id,
            "from_users": "",
            "to_users": "",
            "note": note.note,
            "is_delete": note.is_delete,
            "created_name": note.first_name[0] + " " + note.last_name[0],
            "created_by": note.created_by,
            "full_name": note.first_name + " " + note.last_name,
            "created_date": getTimeAgoValue(note.created_date),
            "created_dt": formatDate(note.created_date, "%d/%m/%Y %H:%M:%S")
        }
        user_notes.append(row)
    return JSONResponse(
        status_code = 200,
        content = {
            "status": True,
            "message": "User Notes",
            "user_notes": user_notes
        }
    )