from date import Date


class Task:
    def __init__(self, task: dict):
        self.object = task
        self.id = task.get('id')
        self.due = self.parse_date(task)
        self.updated = self.parse_date(task)
        self.title = task.get('title') if task.get('title') else 'N/A'
        self.links = task.get('links')
        self.position = task.get('position')
        self.parent = task.get('parent')

    def __repr__(self):
        return f"[{self.due.date}] {self.title.title()}"

    def __gt__(self, other) -> bool:
        if isinstance(other, Task):
            return self.due > other.due
        raise ValueError("Object must be Date()")

    def __lt__(self, other) -> bool:
        if isinstance(other, Task):
            return self.due < other.due
        raise ValueError("Object must be Date()")

    def parse_date(self, data: dict) -> object:
        return Date(data)


class AllTasks:
    def __init__(self, unparsed_tasks):
        self.unparsed_tasks = unparsed_tasks

    @property
    def all(self):
        tasks = []
        for task_data in self.unparsed_tasks:
            task = Task(task_data)
            tasks.append(task)
        return sorted(tasks, reverse=True)

    @property
    def total(self):
        return len(self.all)

    def get_task_filter(self, filter=None) -> object:
        if filter == 'next':
            date = min([task.due.date for task in self.all])
            next = [task for task in self.all if task.due.date == date] # need to get a list
            return next if next else None
        elif filter == 'today':
            return [task for task in self.all if task.due.is_today]
        elif filter == 'tomorrow':
            return [task for task in self.all if task.due.is_tomorrow]
        elif filter == 'this_week':
            return [task for task in self.all if task.due.is_this_week]
        elif filter == 'next_week':
            return [task for task in self.all if task.due.is_next_week]

    @property
    def next(self) -> object:
        return self.get_task_filter(filter='next')

    @property
    def today(self) -> list:
        return self.get_task_filter(filter='today')

    @property
    def tomorrow(self) -> list:
        return self.get_task_filter(filter='tomorrow')

    @property
    def this_week(self) -> list:
        return self.get_task_filter(filter='this_week')

    @property
    def next_week(self) -> list:
        return self.get_task_filter(filter='next_week')
