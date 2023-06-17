from datetime import datetime

from google_calendar import NosotrosCalendar

import appdaemon.plugins.hass.hassapi as hass


class CalendarNosotros(hass.Hass):

	def initialize(self):
		self.calendar = NosotrosCalendar(allow_duplicates=False)
		self.run_every(self.run_daily_callback, "now", 15 * 60)

	def format_data_for_ha(self, events):
		items = []
		for index, event in enumerate(events):
			if event.end.object.replace(tzinfo=None) < datetime.now():
				continue
			else:
				data = {
					'title': event.title,
					'start_time': event.start.time,
					'end_time': event.end.time,
					'start_date': event.start.date,
					'end_date': event.start.date,
					'start_datetime': event.start.date_long,
					'end_datetime': event.end.date_long,
					'location': event.location if event.location else '-',
					'dow': event.start.day_of_week,
					'is_current': event.status.is_ongoing,
					'is_today': event.start.is_today,
					'is_tomorrow': event.start.is_tomorrow,
				}
				items.append(data)
		return items
	
	def data_for_ha(self):
		all_data = {}
		all = self.format_data_for_ha(self.calendar.events.all)
		all_data['next'] = self.format_data_for_ha([self.calendar.events.next])
		all_data['today'] = self.format_data_for_ha(self.calendar.events.today)
		all_data['tomorrow'] = self.format_data_for_ha(self.calendar.events.tomorrow)
		all_data['rest'] = self.format_data_for_ha(self.calendar.events.rest)
		all_data['all'] = all
		
		return all_data

	def format_data(self, events):
		all_data = {}
		next = []
		rest = []
		for index, event in enumerate(events):
			if event.end.object.replace(tzinfo=None) < datetime.now():
				continue
			data = {
				'title': event.title,
				'date': event.start.date,
				'time': event.start.time,
				'start': event.start.time,
				'end': event.end.time,
				'start_date': event.start.date,
				'end_date': event.start.date,
				'location': event.location if event.location else '-',
				'datetime': event.start.date_long,
				'start_datetime': event.start.date_long,
				'end_datetime': event.end.date_long,
				'is_current': event.status.is_ongoing
			}
			if next == []:
				next.append(data)
			else:
				rest.append(data)
		all_data['next'] = [next[0]]
		all_data['rest'] = rest[:9]
		all_data['all'] = [next[0]]
		all_data['all'] += rest[:9]
		return all_data

	def run_daily_callback(self, kwargs):
		print(f'Getting List of all events for calendar "{self.calendar.name}"')
		# data = self.format_data(self.calendar.events.all)
		data = self.data_for_ha()

		self.grab_date = datetime.now().strftime("%d/%m/%Y (%H:%M:%S.%f)")

		self.remove_entity("sensor.appd_nosotros_calendar")

		self.set_state(
			"sensor.appd_nosotros_calendar",
			state='OK',
			attributes={
				'grab': self.grab_date, 
				'events': data,
			})

