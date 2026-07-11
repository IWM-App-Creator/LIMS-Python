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

def formatDate(from_date: str, format: str = "%d/%m/%Y") -> str:
    try:
        source_tz = ZoneInfo(DEFAULT_TZ)
        user_tz = getTimeZone()  # Convert Timezone based on user setting, Default "Australia/Perth"
        if isinstance(from_date, datetime):
            dt = from_date
        else:
            dt = datetime.strptime(from_date, "%Y-%m-%d %H:%M:%S")
        dt = dt.replace(tzinfo = source_tz).astimezone(user_tz)
        return dt.strftime(format)
    except Exception:
        return ""

def getTimeAgoValue(from_date: str) -> str:
    try:
        tz = getTimeZone() # Convert Timezone based on user setting, Default "Australia/Perth"
        if isinstance(from_date, datetime):
            dt = from_date
        else:
            dt = datetime.strptime(from_date, "%Y-%m-%d %H:%M:%S")
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

# %Y-%m-%d	2026-07-08
# %d/%m/%Y	08/07/2026
# %m/%d/%Y	07/08/2026
# %d-%m-%Y	08-07-2026
# %m-%d-%Y	07-08-2026
# %d.%m.%Y	08.07.2026
# %Y/%m/%d	2026/07/08
# %d %b %Y	08 Jul 2026
# %d %B %Y	08 July 2026
# %b %d, %Y	Jul 08, 2026
# %B %d, %Y	July 08, 2026
# %A, %d %B %Y	Wednesday, 08 July 2026
# %a, %d %b %Y	Wed, 08 Jul 2026
# %Y-%m-%d %H:%M:%S	2026-07-08 14:30:45
# %Y-%m-%d %H:%M	2026-07-08 14:30
# %d/%m/%Y %H:%M:%S	08/07/2026 14:30:45
# %d/%m/%Y %H:%M	08/07/2026 14:30
# %m/%d/%Y %I:%M:%S %p	07/08/2026 02:30:45 PM
# %d-%b-%Y %H:%M	08-Jul-2026 14:30
# %d %B %Y %I:%M %p	08 July 2026 02:30 PM
# %H:%M:%S	14:30:45
# %H:%M	14:30
# %I:%M:%S %p	02:30:45 PM
# %I:%M %p	02:30 PM
# %Y	4-digit year	2026
# %y	2-digit year	26
# %m	Month (01-12)	07
# %d	Day (01-31)	08
# %H	Hour (00-23)	14
# %I	Hour (01-12)	02
# %M	Minute	30
# %S	Second	45
# %p	AM/PM	PM
# %a	Short weekday	Wed
# %A	Full weekday	Wednesday
# %b	Short month	Jul
# %B	Full month	July
# %j	Day of year	189
# %U	Week number (Sunday first)	27
# %W	Week number (Monday first)	27
# %f	Microseconds	123456
# %z	UTC offset	+0800
# %Z	Timezone name	AWST