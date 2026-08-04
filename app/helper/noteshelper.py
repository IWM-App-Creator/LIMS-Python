import json
from collections import defaultdict
from app.dbfunctions.notesfunctions import getSmileyNotes, getFromUsersData, getToUsersData

def getNotesUsers(notesps):
    if notesps.note_ids.get() in (None, ""):
        return {}, {}
    from_map = defaultdict(list)
    to_map = defaultdict(list)
    from_rows = getFromUsersData(notesps)
    for row in from_rows:
        fullname = f"{row.first_name} {row.last_name}"
        from_map[row.notes_id].append({
            "user_id": row.id, "initial": row.first_name[0] + row.last_name[0], "fullname": fullname
        })
    to_rows = getToUsersData(notesps)
    for row in to_rows:
        fullname = f"{row.first_name} {row.last_name}"
        to_map[row.notes_id].append({
            "user_id": row.id, "initial": row.first_name[0] + row.last_name[0], "fullname": fullname
        })
    return from_map, to_map

def getSmileyNotesMap(notesps):
    smiledata = getSmileyNotes(notesps)
    smileymap = defaultdict(list)
    for smile in smiledata:
        smileymap[smile.notes_id].append({
            "smiley_id": getattr(smile, "smiley_id", 0),
            "smiley_code": getattr(smile, "smiley_code", ""),
            "notes_id": getattr(smile, "notes_id", 0),
            "created_by": getattr(smile, "created_by", 0),
            "created_name": getattr(smile, "first_name", "") + " " + getattr(smile, "last_name", ""),
        })
    return smileymap

def setNoteInputParam(notesps, params):
    notes_id = params.get("notes_id", 0)
    parent_id = params.get("parent_id", 0)
    view_id = params.get("view_id", 0)
    table_id = params.get("table_id", 0)
    item_ids = params.get("item_ids", [])
    share_users = params.get("share_users", [])
    note = params.get("note", "")
    reminder_date = params.get("reminder_date", None)
    # Handle FormData where share_users is JSON string
    if isinstance(share_users, str):
        try:
            share_users = json.loads(share_users)
        except json.JSONDecodeError:
            # Fallback for comma-separated values
            share_users = [
                {"opt_val": int(x), "type": 0}
                for x in share_users.split(",")
                if x.strip()
            ]
    # Ensure it's a list
    if not isinstance(share_users, list):
        share_users = []
    # Handle FormData where share_users is JSON string
    if isinstance(item_ids, str):
        try:
            item_ids = json.loads(item_ids)
        except json.JSONDecodeError:
            # Fallback for comma-separated values
            item_ids = [x for x in item_ids.split(",") if x.strip()]
    # Ensure it's a list
    if not isinstance(item_ids, list):
        item_ids = []
    notesps.notes_id.set(notes_id)
    notesps.parent_id.set(parent_id)
    notesps.view_id.set(view_id)
    notesps.table_id.set(table_id)
    notesps.item_ids.set(item_ids)
    notesps.note.set(note)
    notesps.share_users.set(share_users)
    notesps.reminder_date.set(reminder_date)