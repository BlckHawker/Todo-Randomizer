# Information for a Task

class Task():
    def __init__(self, name):
        # The name of the task
        self._name = name
        # The date the task was started
        self._start_date = None
        # The date the task was ended (if this is None, then the task has not been complete)
        self._end_date = None
    
    @property
    def name(self):
        return self._name
    
    @property
    def start_date(self):
        return self.get_date(self._start_date)
    
    @property
    def end_date(self):
        return self.get_date(self._end_date)
    
    @start_date.setter
    def start_date(self, new_start_date):
        self._start_date = new_start_date

    @end_date.setter
    def end_date(self, new_start_date):
        self._end_date = new_start_date

    def get_date(self, date):
        return "None" if date is None else date
    
    def export(self):
        return {"name": self.name, "startDate": self.start_date, "endDate": self.end_date}