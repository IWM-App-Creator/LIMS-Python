import os
import json
import secrets
import string
from app.properties.usersproperties import userps
from app.properties.globalproperties import globalps

def setEnvVariables():
    globalps.IS_LOCAL_DEV = os.getenv('IS_LOCAL_DEV')
    globalps.APP_DOMAIN = os.getenv('APP_DOMAIN')
    # globalps.APP_DOMAIN_FRONT = os.getenv('APP_DOMAIN_FRONT')
    # globalps.SESSION_DOMAIN = os.getenv('SESSION_DOMAIN')
    globalps.AI_API_URL = os.getenv('AI_API_URL')
    globalps.ASSET_URL = os.getenv('ASSET_URL')
    globalps.JWT_USER_ID = os.getenv('JWT_USER_ID')

def getHostName(request):
    host = request.headers.get("Host", "")
    hostsd = host.split(":")[0]
    userps.req_host.set(host)
    userps.req_subdomain.set(hostsd.split(".")[0])

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
        if srchval is None or srchkey is None or nested.get(srchkey) == srchval:
            nested[updkey] = updval
            return True
        return False
    elif isinstance(nested, list):
        updated = False
        for item in nested:
            if item.get(srchkey) == srchval or srchval is None:
                item[updkey] = updval
                updated = True
                # Stop after first match only when searching for a value
                if srchval is not None:
                    break
        return updated
    return False

def insertNestedJsonAfter(fulljson: dict, jsonkey: str, srchkey: str, srchval, new_item: dict ):
    nested = fulljson.get(jsonkey)
    if isinstance(nested, dict):
        fulljson[jsonkey] = [nested]
        nested = fulljson[jsonkey]
    if not isinstance(nested, list):
        return False
    for i, item in enumerate(nested):
        if item.get(srchkey) == srchval:
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
        if item.get(srchkey) == srchval:
            nested.insert(i, new_item)
            return True

    return False

def removeNestedJsonVal(fulljson: dict, jsonkey: str, srchkey: str, srchval):
    nested = fulljson.get(jsonkey)
    if isinstance(nested, dict):
        if srchval is None or nested.get(srchkey) == srchval:
            del fulljson[jsonkey]
            return True
        return False
    if not isinstance(nested, list):
        return False
    removed = False
    for i in range(len(nested) - 1, -1, -1):
        if srchval is None or nested[i].get(srchkey) == srchval:
            del nested[i]
            removed = True
            # Remove only the first matching item
            if srchval is not None:
                break
    return removed