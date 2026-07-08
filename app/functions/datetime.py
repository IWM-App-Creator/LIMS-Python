from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
from app.properties.usersproperties import userps

DEFAULT_TZ = "Australia/Perth"
DEFAULT_FORMAT = "%Y-%m-%d %H:%M:%S"

def getTimeZone():
    try:
        tz_name = userps.user_timezone.get()
        if tz_name:
            return ZoneInfo(tz_name)
        return ZoneInfo(DEFAULT_TZ)
    except ZoneInfoNotFoundError:
        return ZoneInfo(DEFAULT_TZ)

def nowWithTimeZone(format: str | None = DEFAULT_FORMAT):
    tz = ZoneInfo(DEFAULT_TZ) # Default "Australia/Perth"
    dt = datetime.now(tz)
    return dt.strftime(format) if format else dt

def formatDate(created_date: str, format: str = "%d/%m/%Y") -> str:
    try:
        source_tz = ZoneInfo(DEFAULT_TZ)
        user_tz = getTimeZone()  # Convert Timezone based on user setting, Default "Australia/Perth"
        dt = datetime.strptime(created_date, "%Y-%m-%d %H:%M:%S")
        dt = dt.replace(tzinfo=source_tz).astimezone(user_tz)
        return dt.strftime(format)
    except Exception:
        return ""
    
def getTimeAgoValue(created_date: str) -> str:
    try:
        tz = getTimeZone() # Convert Timezone based on user setting, Default "Australia/Perth"
        dt = datetime.strptime(created_date, "%Y-%m-%d %H:%M:%S")
        dt = dt.replace(tzinfo = tz)
        now = datetime.now(tz)
        elapsed = int((now - dt).total_seconds())
        seconds = elapsed
        minutes = round(elapsed / 60)
        hours = round(elapsed / 3600)
        days = round(elapsed / 86400)
        if seconds <= 60:
            return f"{seconds} seconds ago"
        elif minutes <= 60:
            return "one minute ago" if minutes == 1 else f"{minutes} minutes ago"
        elif hours <= 24:
            return "an hour ago" if hours == 1 else f"{hours} hours ago"
        elif days <= 7:
            return "yesterday" if days == 1 else dt.strftime("%d/%m/%y")
        return dt.strftime("%d/%m/%y")
    except Exception:
        return ""