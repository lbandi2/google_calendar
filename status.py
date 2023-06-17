from datetime import datetime


class Status:
    def __init__(self, event):
        self.event = event

    @property
    def is_all_day(self):
        return self.event.time.duration() >= 86400

    @property
    def is_finished(self):
        return self.event.start.object.replace(tzinfo=None) < datetime.now() and \
                self.event.end.object.replace(tzinfo=None) < datetime.now()

    @property
    def is_ongoing(self):
        return self.event.start.object.replace(tzinfo=None) <= datetime.now() <= self.event.end.object.replace(tzinfo=None)

    @property
    def is_pending(self):
        return self.event.start.object.replace(tzinfo=None) > datetime.now() and \
                self.event.end.object.replace(tzinfo=None) > datetime.now()

    @property
    def readable(self):
        if self.is_pending:
            return 'pending'
        elif self.is_ongoing:
            return 'ongoing'
        elif self.is_finished:
            return 'finished'
        else:
            raise ValueError('Undefined status for event')
