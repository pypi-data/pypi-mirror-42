import sys
import gitutils
from datetime import datetime
from gitutils.course import Course, CourseManager

def setup_course():
    assert(len(sys.argv) == 2), "Usage: python setup_class.py <optionfile>.json"
    # Creates a default Course Manager
    cmanager = CourseManager()
    # Creates a course using the supplied first argument
    cmanager.setup_course(sys.argv[1])

def verify_course():
    assert(len(sys.argv) == 2), "Usage: python verify_course.py <optionfile>.json"
    # Creates a default Course Manager
    cmanager = CourseManager()
    # Creates a course using the supplied first argument
    cmanager.verifyCourse(sys.argv[1])
