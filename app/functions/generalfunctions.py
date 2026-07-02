from datetime import datetime
import os
from app.properties.globalproperties import globalps

def setEnvVariables():
    globalps.IS_LOCAL_DEV = os.getenv('IS_LOCAL_DEV')
    globalps.APP_DOMAIN = os.getenv('APP_DOMAIN')
    globalps.APP_DOMAIN_FRONT = os.getenv('APP_DOMAIN_FRONT')
    globalps.SESSION_DOMAIN = os.getenv('SESSION_DOMAIN')
    globalps.LOCAL_SUBDOMAIN = os.getenv('LOCAL_SUBDOMAIN')
    globalps.AI_API_URL = os.getenv('AI_API_URL')
    globalps.ASSET_URL = os.getenv('ASSET_URL')
    globalps.JWT_USER_ID = os.getenv('JWT_USER_ID')
