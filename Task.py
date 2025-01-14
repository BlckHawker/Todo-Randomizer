# Information for a Task

class Task():
    def __init__(self, name):
        # The name of the task
        self._name = name
        # The date the task was started
        self.start_date = None
        # The date the task was ended (if this is None, then the task has not been complete)
        self.end_date = None
    
    @property
    def name(self):
        return self._name
    
    def get_start_date(self):
        return self.get_date(self.start_date)


    def get_end_date(self):
        return self.get_date(self.end_date)

    def get_date(self, date):
        if(date is None):
            return "None"
        else:
            # todo replace this with the date format (MM/DD/YYYY)
            pass 