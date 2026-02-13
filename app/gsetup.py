import os
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from datetime import datetime
import pytz


class Creds:
    def __init__(self, scopes=[], credentials_dir=''):
        self.scopes = scopes
        self.token = f'./{credentials_dir}/token.pickle'
        self.credentials = f'./{credentials_dir}/service.json'

    def load_credentials(self):
        creds = None
        if os.path.exists(self.token):
            with open(self.token, 'rb') as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.credentials, self.scopes)
                creds = flow.run_local_server(port=0)
            with open(self.token, 'wb') as token:
                pickle.dump(creds, token)

        return creds


class CredsCalendar(Creds):
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    CREDENTIALS_DIR = 'creds/calendar'

    def __init__(self):
        super().__init__(scopes=self.SCOPES, credentials_dir=self.CREDENTIALS_DIR)

    def service(self):
        creds = self.load_credentials()
        return build('calendar', 'v3', credentials=creds)

    def calendars(self):
        calendars_result = self.service().calendarList().list().execute()
        calendars = calendars_result.get('items', [])
        return {item['id'] : item['summary'] for item in calendars}

    def events(self, cal_id=None, tz='America/Bogota'):
        now = pytz.timezone(tz).localize(
            datetime.utcnow().replace(
                hour=0, 
                minute=0, 
                second=0, 
                microsecond=0
                )).isoformat()
        events_result = self.service().events().list(
            calendarId=cal_id, timeMin=now,
            singleEvents=True,
            orderBy='startTime').execute()
        events = events_result.get('items', [])
        return events


class CredsTasks(Creds):
    SCOPES = ['https://www.googleapis.com/auth/tasks']
    CREDENTIALS_DIR = 'creds/tasks'

    def __init__(self):
        super().__init__(scopes=self.SCOPES, credentials_dir=self.CREDENTIALS_DIR)

    def service(self):
        creds = self.load_credentials()
        return build('tasks', 'v1', credentials=creds)

    def lists(self):
        tasklist_result = self.service().tasklists().list().execute()
        tasklists = tasklist_result.get('items', [])
        return {item['id'] : item['title'] for item in tasklists}

    def tasks(self, list_id=None):
        tasks_result = self.service().tasks().list(
            tasklist=list_id).execute()
        tasks = tasks_result.get('items', [])
        return tasks