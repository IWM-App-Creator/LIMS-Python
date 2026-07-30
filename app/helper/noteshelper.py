from collections import defaultdict
from app.dbfunctions.notesfunctions import getSmileyNotes

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