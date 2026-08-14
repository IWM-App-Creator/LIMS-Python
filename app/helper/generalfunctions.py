import os
import json
import secrets
import string
import shutil
import time
from pathlib import Path
from app.dbfunctions.associationfunctions import getAssociationUsers
from fastapi import UploadFile
from app.properties.usersproperties import userps
from app.properties.viewproperties import viewps
from app.properties.globalproperties import globalps
from app.properties.associationproperties import associationps

def setEnvVariables():
    globalps.APP_NAME = os.getenv('APP_NAME')
    globalps.APP_URL = os.getenv('APP_URL')
    globalps.APP_DOMAIN = os.getenv('APP_DOMAIN')
    globalps.DISABLE_AI_CALL = os.getenv('DISABLE_AI_CALL')
    globalps.AI_API_URL = os.getenv('AI_API_URL')

    globalps.DB_DEBUG_LEVEL = os.getenv('DB_DEBUG_LEVEL') # Debug Level Log, Print etc.
    globalps.IS_LOCAL_DEV = os.getenv('IS_LOCAL_DEV')
    globalps.JWT_USER_ID = os.getenv('JWT_USER_ID')

    globalps.SECRET_KEY = os.getenv('SECRET_KEY') # JWT algorithm used for signing the token
    globalps.ALGORITHM = os.getenv('ALGORITHM') # JWT algorithm used for signing the token
    globalps.ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES') # JWT token expiration time in minutes

def getHostName(request):
    host = request.headers.get("Host", "")
    hostsd = host.split(":")[0]
    userps.req_host.set(host)
    userps.req_subdomain.set(hostsd.split(".")[0])

def uploadFile(ws_url: str, folder: str, file: UploadFile) -> str | None:
    if file is None or not file.filename:
        return None
    destination_path = Path("wsassets/uploads") / ws_url / folder
    destination_path = makeDirectory(destination_path)
    stem = Path(file.filename).stem          # abc
    extension = Path(file.filename).suffix   # .png
    filename = f"{stem}_{int(time.time())}{extension}"
    with open(destination_path / filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return filename

def makeDirectory(path: str | Path) -> Path:
    directory = Path(path)
    directory.mkdir(parents=True, exist_ok=True, mode=0o777)
    # Optional: Set permissions on Linux/macOS
    try:
        os.chmod(directory, 0o777)
    except Exception:
        # Ignored on Windows
        pass
    return directory

def removeDirectory(path: str | Path) -> bool:
    directory = Path(path)
    if directory.exists() and directory.is_dir():
        shutil.rmtree(directory)
        return True
    return False

def removeFile(path: str | Path) -> bool:
    file_path = Path(path)
    if file_path.exists() and file_path.is_file():
        file_path.unlink()
        return True
    return False

def generateRandomString(length: int = 10, hasdigits: int = 0) -> str:
    alphabet = string.ascii_lowercase
    if hasdigits == 1 :
        alphabet = string.ascii_lowercase + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))

def formatUserDisplayName(first_name: str = "", last_name: str = "", format_type: str = "") -> str:
    first_name = first_name or ""
    last_name = last_name or ""
    match format_type.upper():
        case "INITIAL":
            display_name = ""
            if first_name:
                display_name += first_name[0]
            if last_name:
                display_name += last_name[0]
            return display_name
        case "FIRSTNAME":
            return first_name
        case "LASTNAME":
            return last_name
        case _:
            return f"{first_name} {last_name}".strip()

def getUserRoleName(user_role_id: int) -> str:
    return {
        1: "Super Admin",
        2: "User"
    }.get(user_role_id, "No Access")

def getWSUserRole(ws_role_id: int) -> str:
    return {
        1: "Owner",
        2: "User"
    }.get(ws_role_id, "No Access")

def sortObjectsByKey(arr, key, direction = "asc"):
    arr.sort(
        key = lambda x: x.get(key),
        reverse = (direction.lower() == "desc")
    )

def addUpdateJson(data: dict, key: str, value):
    if value not in (None, ""):
        data[key] = value

def removeJsonKey(data: dict, key: str):
    return data.pop(key, None) is not None

def updateNestedJsonVal(fulljson: dict, jsonkey: str, srchkey: str, srchval: str, updkey: str, updval):
    nested = fulljson.get(jsonkey)
    if isinstance(nested, dict):
        if srchval is None or srchkey is None or str(nested.get(srchkey)) == str(srchval):
            nested[updkey] = updval
            return True
        return False
    elif isinstance(nested, list):
        updated = False
        for item in nested:
            if str(item.get(srchkey)) == str(srchval) or srchval is None:
                item[updkey] = updval
                updated = True
                # Stop after first match only when searching for a value
                if srchval is not None:
                    break
        return updated
    return False

def getListJsonVal(fulljson: list, srchkey: str, srchval=None):
    if not isinstance(fulljson, list):
        return None
    for item in fulljson:
        if not isinstance(item, dict):
            continue
        if srchval is None or str(item.get(srchkey)) == str(srchval):
            return item
    return None

def updateListJsonVal(fulljson: list, srchkey: str, srchval, updvals: dict):
    if not isinstance(fulljson, list):
        return False
    for item in fulljson:
        if not isinstance(item, dict):
            continue
        if srchval is None or str(item.get(srchkey)) == str(srchval):
            item.update(updvals)
            return True
    return False

def removeListJsonVal(fulljson: list, srchkey: str, srchval):
    if not isinstance(fulljson, list):
        return False

    for index, item in enumerate(fulljson):
        if not isinstance(item, dict):
            continue

        if str(item.get(srchkey)) == str(srchval):
            fulljson.pop(index)
            return True

    return False

def insertNestedJsonAfter(fulljson: dict, jsonkey: str, srchkey: str, srchval, new_item: dict ):
    nested = fulljson.get(jsonkey)
    if isinstance(nested, dict):
        fulljson[jsonkey] = [nested]
        nested = fulljson[jsonkey]
    if not isinstance(nested, list):
        return False
    for i, item in enumerate(nested):
        if str(item.get(srchkey)) == str(srchval):
            nested.insert(i + 1, new_item)
            return True
    return False

def insertNestedJsonBefore(fulljson: dict, jsonkey: str, srchkey: str, srchval, new_item: dict):
    nested = fulljson.get(jsonkey)
    if isinstance(nested, dict):
        fulljson[jsonkey] = [nested]
        nested = fulljson[jsonkey]
    if not isinstance(nested, list):
        return False
    for i, item in enumerate(nested):
        if str(item.get(srchkey)) == str(srchval):
            nested.insert(i, new_item)
            return True

    return False

def removeNestedJsonVal(fulljson: dict, jsonkey: str, srchkey: str, srchval):
    nested = fulljson.get(jsonkey)
    if isinstance(nested, dict):
        if srchval is None or str(nested.get(srchkey)) == str(srchval):
            del fulljson[jsonkey]
            return True
        return False
    if not isinstance(nested, list):
        return False
    removed = False
    for i in range(len(nested) - 1, -1, -1):
        if srchval is None or str(nested[i].get(srchkey)) == str(srchval):
            del nested[i]
            removed = True
            # Remove only the first matching item
            if srchval is not None:
                break
    return removed

def getLastUpdatedJSON(type: str) -> str:
    metadata = {
        "user_id": int(userps.user_id.get()),
        "view_id": int(viewps.view_id.get()),
        "type": type
    }
    return json.dumps(metadata)

def getSelectedUsers(tmparr: list, view_id: int) -> list:
    share_users = []
    for tmp in tmparr:
        if tmp.get("type", 0) in (0, "0"):
            share_users.append(tmp.get("opt_val"))
        else:
            associationps.is_notify.set(1)
            associationps.col_p_val.set(tmp.get("opt_val"))
            associationps.view_id.set(view_id)
            associationps.fetch_single.set(0)
            associationps.is_distinct.set(1)
            assousers = getAssociationUsers(associationps)
            for assousr in assousers:
                share_users.append(assousr.get("user_id"))
    share_users = list(dict.fromkeys(share_users))
    return share_users

def normalizeJson(value, default=None):
    if default is None:
        default = {}
    if value is None:
        return default
    if isinstance(value, str):
        value = value.strip()
        if not value:
            return default
        try:
            return json.loads(value)
        except (json.JSONDecodeError, TypeError):
            return default
    if isinstance(value, (dict, list, int, float, bool)):
        return value
    return default