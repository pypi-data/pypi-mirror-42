# -*- python-indent-offset: 4; -*-


class TaskNotFoundException(Exception):
    def __init__(self, task_id):
        super().__init__("Task id %d could not be found." % (task_id))


class EntryFoundException(Exception):
    def __init__(self, uuid):
        super().__init__("Entry with uuid %s could not be found." % (uuid))


class ArgumentException(Exception):
    def __init__(self, message):
        super().__init__(message)
