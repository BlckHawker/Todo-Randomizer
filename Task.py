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