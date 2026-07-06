import os
from app.properties.globalproperties import globalps
from app.properties.usersproperties import userps

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
