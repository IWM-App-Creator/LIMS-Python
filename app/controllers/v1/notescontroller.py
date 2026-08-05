import json
from app.utils.common import Request, RequestData, JSONResponse, getTimeAgoValue, raiseAPIError
from app.helper.datetime import formatDate
from app.helper.noteshelper import setNoteInputParam, getSmileyNotesMap, getNotesUsers, saveTableNotes
from app.dbfunctions.logfunctions import saveErrorLogtoDB
from app.dbfunctions.notesfunctions import getNotes
from app.properties.notesproperties import notesps

def getUserNotes(request: Request):
    try:
        params = RequestData.params(request)
        notesps.view_id.set(params.get("view_id", 0))
        notesps.item_id.set(params.get("item_id", 0))
        notesps.showdel.set(params.get("showdel", 0))
        notesarr = getNotes(notesps)
        notesps.note_ids.set([note.notes_id for note in notesarr])
        smilemap = getSmileyNotesMap(notesps)
        from_map, to_map = getNotesUsers(notesps)
        user_notes = []
        for note in notesarr:
            row = {
                "notes_id": note.notes_id,
                "parent_id": note.parent_id,
                "from_users": from_map.get(note.notes_id, []),
                "to_users": to_map.get(note.notes_id, []),
                "note": note.note,
                "is_delete": note.is_delete,
                "created_by": note.created_by,
                "crtd_full_name": note.first_name + " " + note.last_name,
                "crtd_initial_name": note.first_name[0] + note.last_name[0],
                "created_date": getTimeAgoValue(note.created_date),
                "created_dt": formatDate(note.created_date, "%d/%m/%Y %H:%M:%S"),
                "smiley_list": smilemap.get(note.notes_id, [])
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
    except Exception as e:
        saveErrorLogtoDB("Notes", notesps.view_id.get(), "getNotes", str(e)) # Log Error To DB
        raiseAPIError(str(e), 500)

def saveUserNote(request: Request):
    print("saveUserNote --> ")
    try:
        params = RequestData.params(request)
        setNoteInputParam(notesps, params)
        # save note to sys_table_notes
        saveTableNotes(notesps)
        return JSONResponse(
            status_code = 200,
            content = {
                "status": True,
                "message": "Note Saved Successfully"
            }
        )
    except Exception as e:
        saveErrorLogtoDB("Notes", notesps.view_id.get(), "saveUserNote", str(e)) # Log Error To DB
        raiseAPIError(str(e), 500)

def saveNoteEmoji(request: Request):
    print("saveNoteEmoji --> ")
    try:
        params = RequestData.params(request)
        notesps.view_id.set(params.get("view_id", 0))
        notesps.notes_id.set(params.get("notes_id", 0))
        notesps.item_id.set(params.get("item_id", 0))
        notesps.smiley_code.set(params.get("smiley_code", 0))
        saveTableNotes(notesps)
        return JSONResponse(
            status_code = 200,
            content = {
                "status": True,
                "message": "Smile Emoji Saved Successfully"
            }
        )
    except Exception as e:
        saveErrorLogtoDB("Notes", notesps.view_id.get(), "saveNoteEmoji", str(e)) # Log Error To DB
        raiseAPIError(str(e), 500)