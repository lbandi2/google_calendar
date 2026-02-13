# from datetime import tzinfo
# import json
from .date import Date
from .status import Status
from .time_data import TimeData


class Event:
    def __init__(self, event: dict, tz: str = None, is_break=False):
        self.id = event.get('id')
        self.start = self.parse_date(event.get('start'), tz) #TODO: implement localize to return offset aware datetimes
        self.end = self.parse_date(event.get('end'), tz)
        self.location = event.get('location')
        self.title = event.get('summary') if event.get('summary') else 'N/A'
        self.is_break = is_break
        if self.is_break:
            self.title = 'Break'
        self.tz = tz

    def as_dict(self):
        return {
            "title": self.title,
            "start_time": self.start.time,
            "end_time": self.end.time,
            "start_date": self.start.date,
            "end_date": self.start.date,
            "start_datetime": self.start.date_long,
            "end_datetime": self.end.date_long,
            "location": self.location if self.location else '-',
            "duration": self.time.duration(unit='minutes'),
            "dow": self.start.day_of_week,
            "is_current": self.status.is_ongoing,
            "is_today": self.start.is_today,
            "is_tomorrow": self.start.is_tomorrow,
        }

    def __repr__(self):
        return f"[{self.start.date}] {self.start.time}-{self.end.time}: {self.title.encode("utf-8")} ({self.time.duration(unit='minutes')})"

    @property
    def status(self):
        return Status(self)

    @property
    def time(self):
        return TimeData(self)

    @property
    def progress(self):
        """
        Calculates the progress (up to 100%) of current event
        """
        return int((self.time.elapsed() / self.time.duration()) * 100) if self.status.is_ongoing else 0

    def parse_date(self, data: dict, tz) -> object:
        return Date(data, tz)

    def delete(self):
        pass
        # self.google.service.events().delete(calendarId=super(super()).cal_id, eventId=self.id).execute()
        #TODO: Should pass the service somehow


class AllEvents:
    def __init__(self, unparsed_events, tz: str, ignore_all_day_events=False, breaks=False, allow_duplicates=True):
        self.unparsed_events = unparsed_events
        self.ignore_all_day_events = ignore_all_day_events
        self.breaks = breaks
        self.allow_duplicates = allow_duplicates
        self.tz = tz

    def calculate_events(self):
        events = []
        for event_data in self.unparsed_events:
            event = Event(event_data, tz=self.tz)
            if not event.status.is_finished:
                if self.ignore_all_day_events:
                    if not event.status.is_all_day:
                        events.append(event)
                else:
                    events.append(event)
        if not self.allow_duplicates:
            events = self.remove_duplicates(events)
        return events

    def calculate_breaks(self):
        breaks = []
        events = self.calculate_events()
        starts = [event.end.date_long for event in events][:-2]
        ends = [event.start.date_long for event in events][1:]
        for event in zip(starts, ends):
            event_obj = Event(
                    {
                        'start': 
                            {'dateTime': event[0], 'timeZone': 'America/Bogota'},
                        'end': 
                            {'dateTime': event[1], 'timeZone': 'America/Bogota'}
                    }
                )

            if event_obj.start.object >= event_obj.end.object or event_obj.end.time <= event_obj.start.time:
                continue
            else:
                breaks.append(event_obj)
        return breaks

    # def remove_duplicates(self, list_of_events):
    #     prev_titles = []
    #     events = []
    #     for item in list_of_events:
    #         if item.title not in prev_titles:
    #             prev_titles.append(item.title)
    #             events.append(item)
    #     return events

    def remove_duplicates(self, list_of_events):
        prev_titles = []
        events = []
        for item in list_of_events:
            if item.title not in prev_titles:
                prev_titles.append(item.title)
                events.append(item)
        return events

    @property
    def _all(self):
        if not self.breaks:
            return self.calculate_events()
        else:
            return self.calculate_breaks()

    @property
    def all(self):
        # return json.dumps([item.as_dict() for item in self.all], indent=4)
        return [item.as_dict() for item in self._all]

    @property
    def total(self):
        return len(self.all)

    def total_hours(self, events):
        total = 0
        for event in events:
            total += event.time.duration(unit='hours')
        return total

    # def get_event_filter(self, filter=None) -> object:
    #     if filter == 'next':
    #         next = [event for event in self.all if event.status.is_pending]
    #         return next[0] if next else None
    #     elif filter == 'ongoing':
    #         ongoing = [event for event in self.all if event.status.is_ongoing]
    #         return ongoing[0] if ongoing else None
    #     elif filter == 'prev':
    #         return self.finished[-1] if self.finished != [] else None
    #     elif filter == 'today':
    #         return [event for event in self.all if event.start.is_today]
    #     elif filter == 'tomorrow':
    #         return [event for event in self.all if event.start.is_tomorrow]
    #     elif filter == 'finished':
    #         return [event for event in self.all if event.status.is_finished]
    #     elif filter == 'remaining':
    #         return [event for event in self.all if not event.status.is_finished]
    #     elif filter == 'remaining_today':
    #         return [event for event in self.remaining if event.start.is_today and not event.status.is_finished]
    #     elif filter == 'remaining_tomorrow':
    #         return [event for event in self.remaining if event.start.is_tomorrow]
    #     elif filter == 'this_week':
    #         return [event for event in self.all if event.start.is_this_week]
    #     elif filter == 'next_week':
    #         return [event for event in self.all if event.start.is_next_week]
    #     elif filter == 'today_first':
    #         return self.today[0] if self.today != [] else None
    #     elif filter == 'today_last':
    #         return self.today[-1] if self.today != [] else None
    #     elif filter == 'tomorrow_first':
    #         return self.tomorrow[0] if self.tomorrow != [] else None
    #     elif filter == 'tomorrow_last':
    #         return self.tomorrow[-1] if self.tomorrow != [] else None
    #     elif filter == 'rest':
    #         if self.remaining_today != []:
    #             return [
    #                 event for event in self.all
    #                 if event.start.is_today is False and 
    #                 event.status.is_finished is False
    #                 ]
    #         elif self.remaining_tomorrow != []:
    #             return [
    #                 event for event in self.all 
    #                 if event.start.is_tomorrow is False and
    #                 event.status.is_finished is False
    #                 ]
    #         return [event for event in self.all if not event.status.is_finished]

    def get_event_filter(self, filter=None) -> object:
        if filter == 'next':
            events = [event.as_dict() for event in self._all if event.status.is_pending]
            return [events[0]] if events else []
        elif filter == 'ongoing':
            events = [event.as_dict() for event in self._all if event.status.is_ongoing]
            return [events[0]] if events else []
        elif filter == 'prev':
            return [self.finished[-1].as_dict()]
        elif filter == 'today':
            return [event.as_dict() for event in self._all if event.start.is_today]
        elif filter == 'tomorrow':
            return [event.as_dict() for event in self._all if event.start.is_tomorrow]
        elif filter == 'finished':
            return [event.as_dict() for event in self._all if event.status.is_finished]
        elif filter == 'remaining':
            return [event for event in self._all if not event.status.is_finished]
        elif filter == 'remaining_today':
            return [event.as_dict() for event in self.remaining if event.start.is_today and not event.status.is_finished]
        elif filter == 'remaining_tomorrow':
            return [event.as_dict() for event in self.remaining if event.start.is_tomorrow]
        elif filter == 'this_week':
            return [event.as_dict() for event in self._all if event.start.is_this_week]
        elif filter == 'next_week':
            return [event.as_dict() for event in self._all if event.start.is_next_week]
        elif filter == 'today_first':
            return [self.today[0]]
        elif filter == 'today_last':
            return [self.today[-1]]
        elif filter == 'tomorrow_first':
            return [self.tomorrow[0]]
        elif filter == 'tomorrow_last':
            return [self.tomorrow[-1]]
        elif filter == 'rest':
            if self.remaining_today != []:
                return [
                    event.as_dict() for event in self._all
                    if event.start.is_today is False and 
                    event.status.is_finished is False
                    ]
            elif self.remaining_tomorrow != []:
                return [
                    event.as_dict() for event in self._all 
                    if event.start.is_tomorrow is False and
                    event.status.is_finished is False
                    ]
            return [event.as_dict() for event in self._all if not event.status.is_finished]

    @property
    def ongoing(self) -> object:
        return self.get_event_filter(filter='ongoing')

    @property
    def next(self) -> object:
        return self.get_event_filter(filter='next')

    @property
    def prev(self) -> object:
        return self.get_event_filter(filter='prev')

    @property
    def today(self) -> list:
        return self.get_event_filter(filter='today')

    @property
    def tomorrow(self) -> list:
        return self.get_event_filter(filter='tomorrow')

    @property
    def finished(self) -> list:
        return self.get_event_filter(filter='finished')

    @property
    def remaining(self) -> list:
        return self.get_event_filter(filter='remaining')

    @property
    def remaining_today(self) -> list:
        return self.get_event_filter(filter='remaining_today')

    @property
    def remaining_tomorrow(self) -> list:
        return self.get_event_filter(filter='remaining_tomorrow')

    @property
    def this_week(self) -> list:
        return self.get_event_filter(filter='this_week')

    @property
    def next_week(self) -> list:
        return self.get_event_filter(filter='next_week')

    @property
    def today_first(self) -> list:
        return self.get_event_filter(filter='today_first')

    @property
    def today_last(self) -> list:
        return self.get_event_filter(filter='today_last')

    @property
    def tomorrow_first(self) -> list:
        return self.get_event_filter(filter='tomorrow_first')

    @property
    def tomorrow_last(self) -> list:
        return self.get_event_filter(filter='tomorrow_last')

    @property
    def rest(self) -> object:
        return self.get_event_filter(filter='rest')
