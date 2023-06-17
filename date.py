from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from utils import parse_string, get_timezone, convert_date

default1 = {'date': '2022-09-24'}
default2 = {'dateTime': '2022-09-26T09:00:00-05:00', 'timeZone': 'America/Bogota'}
default3 = {'dateTime': '2022-09-23T13:35:00.001Z'}


class Date:
    def __init__(self, dict_data: dict, tz: str):
        self.data = dict_data
        self.string = parse_string(self.data)
        self.tz = tz

    @property
    def object(self) -> datetime:
        return convert_date(self.string, orig_tz=get_timezone(self.data), tz_conversion=self.tz)

    def __repr__(self):
        return self.object.strftime('%Y-%m-%dT%H:%M:%S%z')

    def __add__(self, other) -> object:
        if isinstance(other, timedelta):
            return self.object + other
        raise ValueError("Object must be Date()")

    def __sub__(self, other) -> object:
        if isinstance(other, timedelta):
            return abs(self.object - other)
        elif isinstance(other, Date):
            return abs(self.object - other.object)
        raise ValueError("Object must be Date()")

    def __eq__(self, other) -> bool:
        if isinstance(other, Date):
            return self.object == other.object
        elif isinstance(other, datetime):
            return self.object.date() == other.date()
        raise ValueError("Object must be Date()")

    def __gte__(self, other) -> bool:
        if isinstance(other, Date):
            return self.object > other.object
        elif isinstance(other, datetime):
            return self.object.replace(tzinfo=None) > other
        raise ValueError("Object must be Date()")

    def __lte__(self, other) -> bool:
        if isinstance(other, Date):
            return self.object > other.object
        elif isinstance(other, datetime):
            return self.object.replace(tzinfo=None) > other
        raise ValueError("Object must be Date()")

    @property
    def timezone(self) -> str:
        return self.tz

    @property
    def time(self) -> str:
        return self.object.strftime('%H:%M')

    @property
    def date(self) -> str:
        return self.object.strftime('%Y-%m-%d')

    @property
    def date_long(self) -> str:
        return self.object.strftime('%Y-%m-%dT%H:%M:%S%z')
    
    @property
    def day_of_week(self) -> str:
        day = ['Domingo', 'Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado']
        return day[int(self.object.strftime('%w'))]

    def add(self, **kwargs) -> object:
        dt_object = self.object
        dt_object += timedelta(
            weeks = kwargs.get('weeks') if kwargs.get('weeks') else 0,
            days = kwargs.get('days') if kwargs.get('days') else 0,
            hours = kwargs.get('hours') if kwargs.get('hours') else 0,
            minutes = kwargs.get('minutes') if kwargs.get('minutes') else 0,
            seconds = kwargs.get('seconds') if kwargs.get('seconds') else 0
        )
        dt_object += relativedelta(
            years = kwargs.get('years') if kwargs.get('years') else 0,
            months = kwargs.get('months') if kwargs.get('months') else 0
            )
        return Date(
            {
                'dateTime': dt_object.strftime('%Y-%m-%dT%H:%M:%S%z'),
                'timeZone': self.timezone
            }
            )

    def remove(self, **kwargs) -> object:
        dt_object = self.object
        dt_object -= timedelta(
            weeks = kwargs.get('weeks') if kwargs.get('weeks') else 0,
            days = kwargs.get('days') if kwargs.get('days') else 0,
            hours = kwargs.get('hours') if kwargs.get('hours') else 0,
            minutes = kwargs.get('minutes') if kwargs.get('minutes') else 0,
            seconds = kwargs.get('seconds') if kwargs.get('seconds') else 0
        )
        dt_object -= relativedelta(
            years = kwargs.get('years') if kwargs.get('years') else 0,
            months = kwargs.get('months') if kwargs.get('months') else 0
            )
        return Date(
            {
                'dateTime': dt_object.strftime('%Y-%m-%dT%H:%M:%S%z'),
                'timeZone': self.timezone
            }
            )

    @property
    def is_holiday(self):
        pass # get data from holiday calendar

    @property
    def is_today(self):
        return self.object.replace(tzinfo=None).date() == datetime.now().date()

    @property
    def is_tomorrow(self):
        return self.object.replace(tzinfo=None).date() == (datetime.now().date() + timedelta(days=1))

    @property
    def is_this_week(self) -> bool:
        return datetime.now().strftime('%W') == self.object.strftime('%W')

    @property
    def is_next_week(self) -> bool:
        return (datetime.now() + timedelta(days=7)).strftime('%W') == self.object.strftime('%W')

    @property
    def has_tz(self) -> bool:
        return bool(self.object.tzinfo)

    def remove_tz(self) -> None:
        self.object = self.object.replace(tzinfo=None)

    def time_obj(self) -> datetime:
        return self.object.time()
