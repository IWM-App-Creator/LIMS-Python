import os
import json
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

def addUpdateToJson(generalps, updkey, newval, originaljson):
    generalps.itmjson.set(originaljson)
    generalps.jsonkey.set(updkey)
    generalps.jsonval.set(newval)
    generalps.operation.set("ADD_UPDATE")
    modifyJsonObject(generalps)

def modifyJsonObject(generalps):
    try:
        itmjson = generalps.itmjson.get()
        tmpjson = json.loads(itmjson) if itmjson else {}
        operation = generalps.operation.get()
        jsonkey = generalps.jsonkey.get()
        match operation:
            case "ADD_UPDATE":
                tmpjson[jsonkey] = generalps.jsonval.get()
            case "REMOVE":
                tmpjson.pop(jsonkey, None)
        generalps.itmjson.set(json.dumps(tmpjson))
    except Exception:
        pass

def modifyJsonArray(generalps):
    try:
        itmjson = generalps.itmjson.get()
        tmpjson = json.loads(itmjson) if itmjson else {}
        jsonkey = generalps.jsonkey.get()
        if jsonkey not in tmpjson or not isinstance(tmpjson[jsonkey], list):
            tmpjson[jsonkey] = []
        operation = generalps.operation.get()
        matchkey = generalps.matchkey.get()
        matchvalue = generalps.matchvalue.get()
        match operation:
            case "ADD":
                tmpjson[jsonkey].append(generalps.jsonval.get())
            case "UPDATE":
                for i, row in enumerate(tmpjson[jsonkey]):
                    if row.get(matchkey) == matchvalue:
                        tmpjson[jsonkey][i] = generalps.jsonval.get()
                        break
            case "REMOVE":
                tmpjson[jsonkey] = [
                    row
                    for row in tmpjson[jsonkey]
                    if row.get(matchkey) != matchvalue
                ]
        generalps.itmjson.set(json.dumps(tmpjson))
    except Exception:
        pass

def getJsonObjectByKey(generalps):
    try:
        itmjson = generalps.itmjson.get()
        tmpjson = json.loads(itmjson) if itmjson else {}
        generalps.jsonkeyval.set(
            tmpjson.get(generalps.jsonkey.get(), "")
        )
    except Exception:
        generalps.jsonkeyval.set("")

def sortObjectsByKey(arr, key, direction = "asc"):
    arr.sort(
        key = lambda x: x.get(key),
        reverse = (direction.lower() == "desc")
    )