from dotenv import load_dotenv
from googleapiclient.errors import HttpError

from .gsetup import CredsCalendar
from .event import AllEvents
from .time_data import Timer

load_dotenv()


class Calendar:
    def __init__(
            self, 
            cal_id, 
            tz: str,
            ignore_all_day_events = False, 
            holiday_calendar = None, 
            default_timeout = 5,
            include_breaks = False,
            allow_duplicates = True
            ):
        self.cal_id = cal_id
        self.google = CredsCalendar()
        self.ignore_all_day_events = ignore_all_day_events
        if tz == '':
            tz = 'UTC'
        self.tz = tz
        self.holiday_calendar = holiday_calendar
        self.default_timeout = default_timeout
        self.include_breaks = include_breaks
        self.allow_duplicates = allow_duplicates
        self.timer = Timer(self.default_timeout)
        self._cached_events = AllEvents(self.unparsed_events, tz=self.tz, allow_duplicates=self.allow_duplicates)
        self._cached_breaks = AllEvents(self.unparsed_events, tz=self.tz, breaks=True) if self.include_breaks else None

    @property
    def events(self):
        if not self.timer.is_passed:
            return self._cached_events
        self._cached_events = AllEvents(self.unparsed_events, tz=self.tz)
        self.timer.restart()
        return self._cached_events

    @property
    def breaks(self):
        if not self.timer.is_passed or not self._cached_breaks:
            return self._cached_breaks
        self._cached_breaks = AllEvents(self.unparsed_events, tz=self.tz, breaks=True)
        self.timer.restart()
        return self._cached_breaks

    @property
    def other_cals(self):
        return self.google.calendars()

    @property
    def name(self):
        return self.google.calendars().get(self.cal_id)

    @property
    def unparsed_events(self):
        return self.google.events(cal_id=self.cal_id)

    def refresh(self):
        self.events = AllEvents(self.unparsed_events, tz=self.tz)

    def insert(self, title, start, end):
        event = {
            'summary': title,
            'start': {
                'dateTime': start,
                'timeZone': self.tz,
            },
            'end': {
                'dateTime': end,
                'timeZone': self.tz,
            },
            'reminders': {
                'useDefault': True
            },
        }
        try:
            new_event = self.google.service().events().insert(calendarId=self.cal_id, body=event).execute()
            print('Event created: %s' % (new_event.get('htmlLink')))
        except HttpError:
            print("Insufficient permission to write to this calendar")
