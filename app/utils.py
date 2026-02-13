import re
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

def parse_string(obj):
    if isinstance(obj, dict):
        if 'dateTime' in obj:
            return obj.get('dateTime')
        elif 'date' in obj:
            return obj.get('date')
        elif 'due' in obj:
            return obj.get('due')
        elif 'updated' in obj:
            return obj.get('updated')
    elif isinstance(obj, datetime):
        return obj.strftime('%Y-%m-%dT%H:%M:%S%z')
    raise ValueError("Unrecognized date object")

def get_timezone(obj):
    if isinstance(obj, dict):
        if 'timeZone' in obj:
            return obj.get('timeZone')
    elif isinstance(obj, datetime):
        return obj.tzinfo.zone if obj.tzinfo else None
    return None

def has_date(string: str) -> bool:
    return bool(re.search('\d{4}-\d{2}-\d{2}', string))

def has_time(string: str) -> bool:
    return bool(re.search('\d{2}:\d{2}:\d{2}', string))

# def has_timezone(string: str) -> bool:
#     return bool(re.search('(\+|\-)\d{2}(:|)\d{2}', string))

def has_timezone(string: str) -> bool:
    return bool(re.search('((\+|\-)\d{2}(:|)\d{2}|Z)', string))

def is_utc(string: str) -> bool:
    return bool(string[-1] == 'Z')

# def convert_date(string: str, tz='America/Bogota') -> datetime:
#     if is_utc(string):
#         string = string[:-1]
#     if re.search('\.\d{3}', string):
#         string = string.replace(re.search('\.\d{3}', string).group(), '') # remove microseconds
#     if has_date(string):
#         if has_timezone(string):
#             date = datetime.strptime(string, '%Y-%m-%dT%H:%M:%S%z').replace(tzinfo=None)
#             return pytz.timezone(tz).localize(date)
#         if has_time(string):
#             return datetime.strptime(string, '%Y-%m-%dT%H:%M:%S')
#         return datetime.strptime(string, '%Y-%m-%d')
#     raise ValueError("String does not contain date information")

def convert_date(string: str, orig_tz=None, tz_conversion='') -> datetime:
    if tz_conversion == '':
        tz_conversion = 'UTC'
    if re.search('\.\d{3}', string):
        string = string.replace(re.search('\.\d{3}', string).group(), '') # remove microseconds

    if has_timezone(string):
        if is_utc(string):
            date = datetime.strptime(string[:-1], '%Y-%m-%dT%H:%M:%S').replace(tzinfo=ZoneInfo(orig_tz))
        else:
            date = datetime.strptime(string, '%Y-%m-%dT%H:%M:%S%z')
        return date.astimezone(ZoneInfo(tz_conversion))
    elif has_date(string):
        date = datetime.strptime(string, '%Y-%m-%d')
        return date.astimezone(ZoneInfo(tz_conversion))
    raise ValueError("String does not contain date information")

def convert_time(string: str) -> datetime:
    if has_time(string):
        return datetime.strptime(string, '%H:%M:%S').time()
    raise ValueError("String does not contain time information")

def test_is_now(start: object, end: object) -> bool:
    return start.object.replace(tzinfo=None) < datetime.now() < end.object.replace(tzinfo=None)

# def test_is_today(start: object, offset=0) -> bool:
#     return start.object.replace(tzinfo=None).date() == (datetime.now().date() + timedelta(days=offset))

def test_is_finished(start: object, end: object) -> bool:
    return start.object.replace(tzinfo=None) < datetime.now() and end.object.replace(tzinfo=None) < datetime.now()

def time_to_event_readable(start: object) -> str:
    phrase = ''
    result = int((start.object.replace(tzinfo=None) - datetime.now()).total_seconds())
    month = 2419200
    week = 604800
    day = 86400
    hour = 3600
    minute = 60
    if result / month >= 1:
        phrase += f"{result // month} mes{'es' if (result // month) > 1 else ''} "
        result -= month * (result // month)
    if result / week >= 1:
        phrase += f"{result // week} semana{'s' if (result // week) > 1 else ''} "
        result -= week * (result // week)
    if result / day >= 1:
        phrase += f"{result // day} día{'s' if (result // day) > 1 else ''} "
        result -= day * (result // day)
    if result / hour >= 1:
        phrase += f"{result // hour} hora{'s' if (result // hour) > 1 else ''} "
        result -= hour * (result // hour)
    if result / minute >= 1:
        phrase += f"{result // minute} minuto{'s' if (result // minute) > 1 else ''} "
    return phrase.rstrip()

def time_remaining(end):
    return (end - datetime.now()).total_seconds()