from datetime import datetime
from zoneinfo import ZoneInfo

PERTH_TZ = ZoneInfo("Australia/Perth")

def nowWithTimeZone(format: None):
    print("nowWithTimeZone --> ", datetime.now(PERTH_TZ))
    return datetime.now(PERTH_TZ)
    # Usage 
    # read_date = now().strftime("%Y-%m-%d %H:%M:%S")
    # created_date = now()

def getTimeAgoValue(created_date: str) -> str:
    try:
        dt = datetime.strptime(created_date, "%Y-%m-%d %H:%M:%S")
        dt = dt.replace(tzinfo=PERTH_TZ)
        now = datetime.now(PERTH_TZ)
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