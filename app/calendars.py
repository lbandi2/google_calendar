from dotenv import load_dotenv
import os

from .google_calendar import Calendar

load_dotenv()

tz_bogota = 'America/Bogota'


class HolidaysCo(Calendar):
    CAL = os.getenv('CAL_HOLIDAYS_CO')

    def __init__(self, tz=tz_bogota):
        super().__init__(cal_id=self.CAL, ignore_all_day_events=False, tz=tz)

class HolidaysAr(Calendar):
    CAL = os.getenv('CAL_HOLIDAYS_AR')

    def __init__(self, tz=tz_bogota):
        super().__init__(cal_id=self.CAL, ignore_all_day_events=False, tz=tz)

class HolidaysUs(Calendar):
    CAL = os.getenv('CAL_HOLIDAYS_US')

    def __init__(self, tz=tz_bogota):
        super().__init__(cal_id=self.CAL, ignore_all_day_events=False, tz=tz)

class Viajes(Calendar):
    CAL = os.getenv('CAL_VIAJES')

    def __init__(self, tz=tz_bogota):
        super().__init__(cal_id=self.CAL, ignore_all_day_events=False, tz=tz)


class Nosotros(Calendar):
    CAL = os.getenv('CAL_NOSOTROS')

    def __init__(self, tz=tz_bogota, allow_duplicates=False):
        super().__init__(cal_id=self.CAL, ignore_all_day_events=False, tz=tz, allow_duplicates=allow_duplicates)


class IM(Calendar):
    CAL = os.getenv('CAL_IM')

    def __init__(self, tz=tz_bogota):
        super().__init__(cal_id=self.CAL, ignore_all_day_events=True, include_breaks=True, tz=tz)


class Velez(Calendar):
    CAL = os.getenv('CAL_VELEZ')

    def __init__(self, tz=tz_bogota):
        super().__init__(cal_id=self.CAL, ignore_all_day_events=True, tz=tz)


class WC(Calendar):
    CAL = os.getenv('CAL_WC')

    def __init__(self, tz=tz_bogota):
        super().__init__(cal_id=self.CAL, ignore_all_day_events=True, tz=tz)

