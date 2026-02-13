from dotenv import load_dotenv
import os

from .gsetup import CredsTasks
from .task import AllTasks

load_dotenv()


class TaskList:
    def __init__(self, list_id=os.getenv('TASKS_MAIN')):
        self.list_id = list_id
        self.google = CredsTasks()

    @property
    def other_lists(self):
        return self.google.lists()

    @property
    def name(self):
        return self.google.lists().get(self.list_id)

    @property
    def unparsed_tasks(self):
        return self.google.tasks(list_id=self.list_id)

    @property
    def tasks(self):
        return AllTasks(self.unparsed_tasks)