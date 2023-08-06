# -*- coding: utf-8 -*-
"""AssignmentManager and LabManager classes."""
# TODO:
#   [ ] - Sign in as gitlabadm and look for system hook setting
#   [ ] - Create a test 'hook server' and see if it works
#   [ ] -
import json
from datetime import datetime
from pathlib import Path


class AssignmentManager:
    """Handles common Assignment manipulation tasks."""

    def __init__(self, course_name):
        """Set up Gitlab and gathers instructor information."""
        self.course_name = course_name

    def create(self, *, tag, due, mimir_id=None):
        """Create an assignment for this course."""
        course = self.course_name
        assignments_dir = Path.home() / 'courses' / course / 'assignments'
        assignment_dir = assignments_dir / tag

        if not Path(assignment_dir).exists():
            Path(assignment_dir).mkdir()

        output_dict = {}
        output_dict['course_name'] = course
        output_dict['tag_name'] = tag
        output_dict['due_date'] = due.isoformat()
        if mimir_id is not None:
            output_dict['mimir_id'] = mimir_id

        assignment_filename = assignment_dir / (tag + '.json')
        with open(assignment_filename, 'w+') as assignment_file:
            json.dump(output_dict, assignment_file, indent=2, sort_keys=True)


class LabManager:
    """Handles common Lab manipulation tasks."""

    def __init__(self, course_name):
        """Set up Gitlab and gathers instructor information."""
        self.course_name = course_name

    def create(self, *, tag, due, mimir_id=None):
        """Create a lab for this course."""
        course = self.course_name
        labs_dir = Path.home() / 'courses' / course / 'labs'
        lab_dir = labs_dir / tag

        if not Path(lab_dir).exists():
            Path(lab_dir).mkdir()

        output_dict = {}
        output_dict['course_name'] = course
        output_dict['tag_name'] = tag
        output_dict['due_date'] = due.isoformat()
        if mimir_id is not None:
            output_dict['mimir_id'] = mimir_id

        lab_filename = lab_dir / (tag + '.json')
        with open(lab_filename, 'w+') as lab_file:
            json.dump(output_dict, lab_file, indent=2, sort_keys=True)
