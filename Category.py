from Task import Task
# Category object that will hold the list of Tasks

class Category():
    def __init__(self, name):
        # The name of the category
        self._name = name

        # A list of back logged tasks
        self._backlogged_tasks = []
        
        # A list of complete tasks
        self._complete_tasks = []

        # A current task
        self._current_task = None

    @property
    def current_task(self):
        return self._current_task
    
    @property 
    def complete_tasks(self):
        return self._complete_tasks
    
    @current_task.setter
    def current_task(self, new_current_task):
        self._current_task = new_current_task
    
    @property
    def backlogged_tasks(self):
        return self._backlogged_tasks
    
    @property
    def name(self):
        return self._name
    
    def add_task_to_backlog(self, new_task: Task):
        # verify the new task does not have the same name as the current task 
        error_str = f'Cannot add a task with the name \"{new_task.name}\" in the category \"{self._name}\" as a task with that name already exists'
        if(self.current_task is not None and new_task.name.upper() == self.current_task.name.upper()):
            raise(Exception(error_str))
        
        # verify the new task does not have the same name as a task within the backlog
        if(any(t.name.upper() == new_task.name.upper() for t in self._backlogged_tasks)):
            raise(Exception(error_str))
        
        # verify the new task does not have the same name as a task within the backlog
        if(any(t.name.upper() == new_task.name.upper() for t in self._complete_tasks)):
            raise(Exception(error_str))

        self._backlogged_tasks.append(new_task)

    def set_task_as_current_task(self, new_task: Task):
        # verify the new task is in the back logged list
        task_in_backlog_list = any(t.name == new_task.name for t in self._backlogged_tasks)

        if(not task_in_backlog_list):
            raise Exception(f'A task named \"{new_task.name}\" could not be found in the category named \"{self._name}\"')

        # if there is a current task, add it to the back log
        if(self._current_task is not None):
            old_current_task = self._current_task
            self._current_task = None
            self.add_task_to_backlog(new_task=old_current_task)

        # set the new task as the current task
        self._current_task = new_task

        # remove the new current task from the backlogged tasks list
        self._backlogged_tasks.remove(new_task)

    def add_task_as_complete(self):
        # if the current task is None, throw exception
        if(self.current_task is None):
            raise Exception(f'The current task in the \"{self.name}\" category is None. Unable to set it as complete')
        
        # add the old current task to the complete list
        self._complete_tasks.append(self.current_task)

        # set the old current task to None
        self.current_task = None