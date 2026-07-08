from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

DEFAULT_TZ = "Australia/Perth"
DEFAULT_FORMAT = "%Y-%m-%d %H:%M:%S"

def getTimeZone(timezone: str | None = None):
    try:
        tz = ZoneInfo(timezone or DEFAULT_TZ)
    except ZoneInfoNotFoundError:
        tz = ZoneInfo(DEFAULT_TZ)
    return tz
    
def nowWithTimeZone(format: str | None = DEFAULT_FORMAT, timezone: str | None = None):
    tz = getTimeZone(timezone)
    dt = datetime.now(tz)
    return dt.strftime(format) if format else dt

def formatDate(created_date: str, fmt: str = "%d/%m/%Y", timezone: str | None = None ) -> str:
    try:
        tz = getTimeZone(timezone)
        dt = datetime.strptime(created_date, "%Y-%m-%d %H:%M:%S")
        dt = dt.replace(tzinfo=DEFAULT_TZ).astimezone(tz)
        return dt.strftime(fmt)
    except Exception:
        return ""
    
def getTimeAgoValue(created_date: str, timezone: str | None = None ) -> str:
    try:
        tz = getTimeZone(timezone)
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