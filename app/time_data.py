from datetime import datetime, timedelta

class TimeData:
    def __init__(self, event):
        self.event = event

    def unit_changer(func):
        def wrapper(self, unit='seconds'):
            units = {
                'seconds': 1,
                'minutes': 60,
                'hours': 3600
            }
            return func(self, units.get(unit))
        return wrapper

    @unit_changer
    def duration(self, unit=1) -> int:
        decimals = 1 if unit == 3600 else 0
        return round((self.event.start - self.event.end).total_seconds() / unit, decimals)

    @unit_changer
    def remaining(self, unit=1) -> int:
        result = (self.event.end.object.replace(tzinfo=None) - datetime.now()).total_seconds()
        return round(result / unit, 2)\
            if self.event.start.object.replace(tzinfo=None)\
            <= datetime.now() <= \
            self.event.end.object.replace(tzinfo=None) else None

    @unit_changer
    def elapsed(self, unit=1) -> int:
        result = (datetime.now() - self.event.start.object.replace(tzinfo=None)).total_seconds()
        return round(result / unit, 2)\
            if self.event.start.object.replace(tzinfo=None)\
            <= datetime.now() <= \
            self.event.end.object.replace(tzinfo=None) else None

    @unit_changer
    def to_start(self, unit=1):
        result = (self.event.start.object.replace(tzinfo=None) - datetime.now()).total_seconds()
        return round(result / unit, 2)\
            if result > 0 else None


class Timer:
    def __init__(self, timer=5):
        self.start_time = datetime.now()
        self.timer = timer

    @property
    def is_passed(self):
        return (self.start_time + timedelta(minutes=self.timer)) <= datetime.now()

    def restart(self):
        self.start_time = datetime.now()