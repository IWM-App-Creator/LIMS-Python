import json
from app.helper.generalfunctions import getSelectedUsers
from bs4 import BeautifulSoup
from collections import defaultdict
from app.dbfunctions.notesfunctions import getSmileyNotes, getFromUsersData, getToUsersData, insertUpdateNotes, getSmileyData, insertUpdateEmoji
from app.dbfunctions.notificationfunctions import insertUpdateNotification
from app.properties.notificationproperties import notifyps

def getNotesUsers(notesps):
    if notesps.note_ids.get() in (None, ""):
        return {}, {}
    from_map = defaultdict(list)
    to_map = defaultdict(list)
    if notesps.flag.get() == "":
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
        share_users = json.loads(share_users)
    # Ensure it's a list
    if not isinstance(share_users, list):
        share_users = []
    # Handle FormData where share_users is JSON string
    if isinstance(item_ids, str):
        item_ids = item_ids.split(",")
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

def saveTableNotes(notesps):
    view_id = int(notesps.view_id.get() or 0)
    table_id = int(notesps.table_id.get() or 0)
    item_ids = notesps.item_ids.get()
    note = notesps.note.get()
    notesps.note_txt.set(BeautifulSoup(note, "html.parser").get_text())
    tmparr = notesps.share_users.get()
    share_users = getSelectedUsers(tmparr, view_id)
    if notesps.reminder_date.get() not in (None, ""):
        notifyps.created_date.set(notesps.reminder_date.get())
    # insert or update note for each item_id to table notes
    for item_id in item_ids:
        if item_id:
            notesps.item_id.set(item_id)
            new_notes_id = insertUpdateNotes(notesps)
            # Save Notifications for each item_id and share_user
            notifyps.noti_type.set("View")
            notifyps.title.set(new_notes_id)
            notifyps.message.set(note)
            notifyps.msg_data.set("")
            notifyps.item_id.set(item_id)
            notifyps.view_id.set(view_id)
            notifyps.table_id.set(table_id)
            notifyps.notes_id.set(new_notes_id)
            notifyps.is_new.set(1)
            for usr in share_users:
                notifyps.to_user_id.set(usr)
                insertUpdateNotification(notifyps)

def saveEmojiDB(notesps):
    smiley_code = int(notesps.smiley_code.get() or 0)
    smile_data = getSmileyData(notesps)
    if smile_data not in (None, "", ()):
        notesps.smiley_id.set(getattr(smile_data, "smiley_id", 0))
        notesps.upd_vals.set({"smiley_code": smiley_code})
        if getattr(smile_data, "smiley_code", 0) == smiley_code:
            notesps.upd_vals.set({"is_delete": 1})
    smiley_id = insertUpdateEmoji(notesps)
    return smiley_id