from collections import defaultdict
from app.dbfunctions.notesfunctions import getSmileyNotes, getFromUsersData, getToUsersData

def getNotesUsers(notesps):
    from_map = defaultdict(list)
    to_map = defaultdict(list)
    from_rows = getFromUsersData(notesps)
    for row in from_rows:
        fullname = f"{row.first_name} {row.last_name}"
        from_map[row.notes_id].append(
            f"{row.id}|{row.first_name[:1]}{row.last_name[:1]}|{fullname}|{row.is_read}"
        )
    to_rows = getToUsersData(notesps)
    for row in to_rows:
        fullname = f"{row.first_name} {row.last_name}"
        to_map[row.notes_id].append(
            f"{row.id}|{row.first_name[:1]}{row.last_name[:1]}|{fullname}|{row.is_read}"
        )
    return from_map, to_map

def getSmileyNotesMap(notesps):
    print("getSmileyNotes --> ")
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