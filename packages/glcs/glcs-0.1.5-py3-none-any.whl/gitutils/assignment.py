# TODO:
#   [ ] - Sign in as gitlabadm and look for system hook setting
#   [ ] - Create a test 'hook server' and see if it works
#   [ ] -
import gitlab
import hashlib
from time import time

class AssignmentManager:
    """Handles common Assignment manipulation tasks like retrieving,
    searching, and deleting of Assignments.
    """

    def __init__(self):
        pass


class Assignment:

    def __init__(self, location, due_date, tag_name):
        self.name = tag_name
        self.location = location
        self.due_date = due_date
