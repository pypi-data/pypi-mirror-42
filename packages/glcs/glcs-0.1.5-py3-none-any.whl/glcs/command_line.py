# -*- coding: utf-8 -*-
"""Command line utilities for the package."""
import sys
import json
from datetime import datetime
from pathlib import Path
from .utils import tryinput
from .course import CourseManager
from .assignment import AssignmentManager, LabManager


def setup_course():
    """Set up a specific course."""
    assert(len(sys.argv) == 2), "Usage: setup-course <coursename>"

    course_name = sys.argv[1]

    options = {}
    if course_config_exists(course_name):
        config_path = Path.home() / 'courses' / (course_name+'.cfg')
        print("Saved course configuration found: ", config_path)
        if reuse_config():
            options = get_course_config(course_name)
        else:
            options = create_course_config(course_name)
    else:
        print("No configuration file found for course", course_name)
        options = create_course_config(course_name)

    cmanager = CourseManager()
    # Creates a course using the supplied first argument
    cmanager.setup_course(options)


def verify_course():
    """Verify a specific course."""
    assert(len(sys.argv) == 2), "Usage: verify-course <coursename>"
    course_name = sys.argv[1]
    options = get_course_config(course_name)
    assert options is not None, \
        "Could not find course configuration file for course " + course_name
    # Creates a default Course Manager
    cmanager = CourseManager()
    # Creates a course using the supplied first argument
    cmanager.verifyCourse(options)


def add_assignment():
    """Add an assignment to an already created course."""
    if len(sys.argv) <= 1:
        course_name = tryinput("Coursename: ")
        amanager = AssignmentManager(course_name)
        tag_name = tryinput("Gitlab tag/assignment name (should be the " +
                            "same as assignment directory): ")
        due_date = tryinput("Due date (e.g. 09/25/19-23:59:00): ")
        due_date = datetime.strptime(due_date, "%m/%d/%y-%H:%M:%S")
        mimir_id = tryinput("Mimir project id (or 'none'): ")
        if mimir_id.strip() == 'none':
            mimir_id = None
        amanager.create(tag=tag_name, due=due_date, mimir_id=mimir_id)
    else:
        course_name = get_named_arg('-c', or_die=True)
        amanager = AssignmentManager(course_name)
        tag_name = get_named_arg('-t', or_die=True)
        due_date = get_named_arg('-d', or_die=True)
        due_date = datetime.strptime(due_date, "%m/%d/%y-%H:%M:%S")
        mimir_id = get_named_arg('-m')
        amanager.create(tag=tag_name, due=due_date, mimir_id=mimir_id)


def add_lab():
    """Add a lab to an already created course."""
    if len(sys.argv) <= 1:
        course_name = tryinput("Coursename: ")
        lmanager = LabManager(course_name)
        tag_name = tryinput("Gitlab tag/lab name (should be the " +
                            "same as assignment directory): ")
        due_date = tryinput("Due date (e.g. 09/25/19-23:59:00): ")
        due_date = datetime.strptime(due_date, "%m/%d/%y-%H:%M:%S")
        mimir_id = tryinput("Mimir project id (or 'none'): ")
        if mimir_id.strip() == 'none':
            mimir_id = None
        lmanager.create(tag=tag_name, due=due_date, mimir_id=mimir_id)
    else:
        course_name = get_named_arg('-c', or_die=True)
        lmanager = LabManager(course_name)
        tag_name = get_named_arg('-t', or_die=True)
        due_date = get_named_arg('-d', or_die=True)
        due_date = datetime.strptime(due_date, "%m/%d/%y-%H:%M:%S")
        mimir_id = get_named_arg('-m')
        lmanager.create(tag=tag_name, due=due_date, mimir_id=mimir_id)


###############################################################################
#   Command-line specific utility functions
###############################################################################


def reuse_config():
    """Ask if the user would like to reuse the same configuration."""
    reuse = ""
    while (reuse.lower() != 'y' and reuse.lower() != 'n'):
        reuse = tryinput("Would you like to reuse this configuration?" +
                         "(Y/n) ")

    return reuse.lower() == 'y'


def get_course_config(course_name):
    """Return the configuration of the given course as a dictionary."""
    if course_config_exists(course_name):
        config_path = Path.home() / 'courses' / (course_name+'.cfg')
        options = {}
        with open(config_path) as config_file:
            options = json.load(config_file)
        return options

    return None


def course_config_exists(course_name):
    """Return whether the course config exists or not."""
    config_path = Path.home() / 'courses' / (course_name+'.cfg')
    return Path(config_path).exists()


def create_course_config(course_name):
    """Create a course config file with for the given coursename."""
    options = {}
    options['course_name'] = course_name
    options['roster_file'] = tryinput("Roster file path? " +
                                      " (path is relative to ~/) ")
    config_file = Path.home() / 'courses' / (course_name+'.cfg')
    graders = []
    print("Grader gitlab username(s)? Separate multiple with a comma " +
          "i.e. amf2015,eap2006")
    graders = tryinput("> ").split(',')
    graders = [grader.strip() for grader in graders]
    options['grader_usernames'] = graders
    options['master_project_id'] = tryinput("ID of project to be forked " +
                                            "to all students? ")

    access = ''
    while (access.lower() != 'm' and access.lower() != 'd'):
        print("What access level should students have to their project? " +
              "(M)aintainer/(D)eveloper")
        access = tryinput("> ")
    if access == 'm':
        options['subgroup_access'] = gitlab.MAINTAINER_ACCESS
    else:
        options['subgroup_access'] = gitlab.DEVELOPER_ACCESS

    access = ''
    while (access.lower() != 'm' and access.lower() != 'd'):
        print("What access lvl should graders have to student projects?" +
              " (M)aintainer/(D)eveloper")
        access = tryinput("> ")
    access = access.lower()
    if access == 'm':
        options['grader_access'] = gitlab.MAINTAINER_ACCESS
    elif access == 'd':
        options['grader_access'] = gitlab.DEVELOPER_ACCESS

    with open(config_file, 'w+') as opt:
        json.dump(options, opt, indent=2, sort_keys=True)
    print("Configuration saved to ", config_file)

    return options


def get_named_arg(arg_name, or_die=False):
    """Get a named argument from the arguments passed from the terminal.

    `add-lab -c cs416`, get_named_arg('-c') would return `cs416`
    `add-lab -c cs416`, get_named_arg('-t', or_die=True) would return error
    `add-lab -c cs416`, get_named_arg('-c', or_die=True) would return `cs416`
    """
    next_one = False
    for arg in sys.argv:
        if next_one:
            return arg
        if arg == arg_name:
            next_one = True
    assert (not or_die or next_one), "No named argument " + arg_name + " found"
    return None
