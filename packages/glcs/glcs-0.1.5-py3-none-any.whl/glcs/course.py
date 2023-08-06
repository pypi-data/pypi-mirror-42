# -*- coding: utf-8 -*-
"""CourseManager and Course classes."""
import sys
import json
import os
import getpass
from pathlib import Path
import gitlab
from gitlab import Gitlab
import jinja2
from .student import Student
from .groups import Group


def parse_roster(gl, roster_file):
    """Parse the roster file into a set of Student objects."""
    students = []
    enrolled_list = roster_to_enrolled_list(roster_file)
    for enrolled in enrolled_list:
        # create a student using the line we parsed
        student = Student(gl, enrolled)
        # add the student to the list
        students.append(student)
    return students


def parse_students_file(gl, course_name):
    """Parse the students file and create a list of students."""
    course_dir = Path.home() / 'courses' / course_name
    students_file = course_dir / 'students' / 'students.json'
    student_list = []
    students = {}
    with open(students_file) as opts:
        students = json.load(opts)
    for student in students:
        student = Student(gl, from_dict=students[student])
        student_list.append(student)

    return student_list


def roster_to_enrolled_list(roster_file):
    """Read in a rosterfile and convert it into a list of dictionaries.

    Each dictionary represents a student enrolled in the course.
    """
    with open(roster_file, 'r') as roster:
        students = []
        for line in roster:
            if not line.strip():
                continue
            line = line.split("|")
            student = {}
            student['username'] = line[0]
            student['year'] = line[1][:4]
            student['month'] = line[1][-2:]
            student['major'] = line[2]
            student['classnum'] = line[3]
            student['labnum'] = line[4]
            student['lname'] = line[6]
            student['fname'] = line[7]
            student['mname'] = line[8]
            student['email'] = line[16]
            students.append(student)

    # make sure to close the file, then return the list of students
    roster.close()
    return students


class CourseManager:
    """Simplifies the handling of courses.

    Supplies a set of common functions for manipulating courses.
    """

    def __init__(self, server='gitlabt',
                 conf=Path.home() / '.python-gitlab.cfg'
                 ):
        """Set up Gitlab and gathers instructor information."""
        # Save the server and settings file
        self.server = server
        # Connect using the specified server and config file
        self.gl = Gitlab.from_config(server, [conf])
        # Make sure the gl.user object exists
        self.gl.auth()
        # Save the current user as the instructor
        # (Assumes its the insctructors config file)
        self.instructor = self.gl.user

    def setup_course(self, options):
        """Create a course from a set of course options and a class rosterfile.

        Runs verifyCourse after course creation.
        """
        gl = self.gl

        options['instructor'] = self.instructor
        course = Course(gl, options)
        course.setup()
        self.verifyCourse(options)

    def verifyCourse(self, options):
        """Verify that a course was set up with the proper settings/users."""
        # Parse through the options file
        gl = self.gl
        options['instructor'] = self.instructor
        className = options["course_name"]
        project_id = options["master_project_id"]
        masterproj = gl.projects.get(project_id)
        project_name = masterproj.name
        access_level_conv = {
            10: "GUEST_ACCESS",
            20: "REPORTER_ACCESS",
            30: "DEVELOPER_ACCESS",
            40: "MAINTAINER_ACCESS",
            50: "OWNER_ACCESS"
        }

        group = Group(gl, className)

        # Parse the roster file and get a list of students
        students = parse_students_file(gl, className)

        # Grab the subgroups in the group
        subgroups = group.list_subgroups()
        output_list = []

        incorrect_student_settings = 0
        correct_student_settings = 0

        errorLog = []
        userNameList = []
        for student in students:
            userNameList.append(student.username)
        # Check if list of students is in the group
        for student in students:
            output_dictionary = {
                "Username": "",
                "Project": "",
                "Sub_group_access": "",
                "Visibility": "",
                "Graders": {},
                "incorrect_settings": "",
                "correct_settings": ""
            }

            name = student.username
            output_dictionary["Username"] = name
            isMember = False
            # Go through each subgroup and match with each user to get info
            for sub in subgroups:
                if sub.name not in userNameList:
                    error = "has an account in gitlab but isn't in the roster"
                    if (sub.name + error) not in errorLog:
                        incorrect_student_settings += 1
                        errorLog.append(sub.name + error)
                if sub.name == name:
                    isMember = True
                    real_group = gl.groups.get(sub.id)
                    visibility = sub.visibility
                    project = real_group.search('projects', project_name)
                    path = project[0]['path_with_namespace']
                    sub_mem = real_group.members.list()
                    for mem in sub_mem:
                        if mem.username == name:
                            sub_access = mem.access_level
                            if sub_access == options['subgroup_access']:
                                output_dictionary["Sub_group_access"] = str(access_level_conv[sub_access])
                            else:
                                output_dictionary["Sub_group_access"] = "NOT " + str(access_level_conv[options["subgroup_access"]])
                                output_dictionary["incorrect_settings"] = True
                        else:
                            for graders in options["grader_usernames"]:
                                if (mem.username not in options["grader_usernames"] and mem.access_level == options['grader_access']):
                                    if (name + " has unnecessary grader, " + mem.username not in errorLog):
                                        errorLog.append(name + " has unnecessary grader, " + mem.username)
                                if graders == mem.username:
                                    grader_name = mem.username
                                    grader_sub_access = mem.access_level

                                    # Check access level of grader
                                    if grader_sub_access == options['grader_access']:
                                        output_dictionary["Graders"][grader_name] = str(access_level_conv[grader_sub_access])
                                    else:
                                        output_dictionary["Graders"][grader_name] = str(access_level_conv[grader_sub_access])
                                        output_dictionary["incorrect_settings"] = True
                                else:
                                    print("Not a grader: " + str(mem.username))
                                    print("Expected grader: " + str(graders))

                    if (len(output_dictionary["Graders"]) == 0 and len(options['grader_usernames']) > 0):
                        output_dictionary["Graders"] = "None"
                        output_dictionary["incorrect_settings"] = True

                    # Check if user has visibility set to private
                    if visibility == 'private':
                        output_dictionary["Visibility"] = str(visibility)
                    else:
                        output_dictionary["Visibility"] = str(visibility)
                        output_dictionary["incorrect_settings"] = True

                    # Check if user has projects in their subgroup
                    expected_path = options['course_name'] + "/" + student.username + "/" + project_name
                    if path.lower() == expected_path.lower():
                        output_dictionary["Project"] = project_name
                    else:
                        output_dictionary["Project"] = "NOT " + project_name
                        output_dictionary["incorrect_settings"] = True

            if not isMember:
                notMember = name + " is in the roster file but doesn't have an account in gitlab"
                errorLog.append(notMember)

            for graders in options["grader_usernames"]:
                if graders not in output_dictionary["Graders"]:
                    output_dictionary["incorrect_settings"] = True

            if output_dictionary["incorrect_settings"] == "":
                output_dictionary["correct_settings"] = True
                output_dictionary["incorrect_settings"] = False
                correct_student_settings = correct_student_settings + 1
            else:
                output_dictionary["correct_settings"] = False
                incorrect_student_settings = incorrect_student_settings + 1
            output_list.append(output_dictionary)

        render_vars = {
            "expected": options, "users": output_list,
            "incorrect_settings": incorrect_student_settings,
            "correct_settings": correct_student_settings, "expected_project": project_name,
            "expected_sub_access": access_level_conv[options['subgroup_access']],
            "expected_grader_access": access_level_conv[options['grader_access']],
            "errorLog": errorLog
        }

        script_path = os.path.dirname(os.path.realpath(__file__))
        home_path = str(Path.home())
        template_file_location = os.path.join(script_path, 'templates')
        rendered_file_path = os.path.join(home_path, className+"-setup-results.html")
        environment = jinja2.Environment(loader=jinja2.FileSystemLoader(template_file_location))
        output_text = environment.get_template('verify_output.html').render(render_vars)
        with open(rendered_file_path, "w+") as result_file:
            result_file.write(output_text)


class Course:
    """Handles Course-wide functions and data."""

    def __init__(self, gl, options):
        """Read the supplied options file and gets a list of students."""
        self.students = dict()
        self.graders = []
        self.group = None
        self.student_list = []
        self.students_by_id = dict()
        self.instructor = options['instructor']
        self.course_name = options['course_name']
        self.options = options
        self.master_proj = ""
        self.gl = gl
        self.dir = {}
        self.dir['course'] = Path.home() / 'courses' / self.course_name
        self.dir['students'] = self.dir['course'] / 'students'
        self.dir['assignments'] = self.dir['course'] / 'assignments'
        self.dir['labs'] = self.dir['course'] / 'labs'

        students_file = self.dir['students'] / 'students.json'
        if not Path(students_file).exists():
            self.student_list = parse_roster(gl, options['roster_file'])
            output_dict = {}
            for student in self.student_list:
                output_dict[student.username] = student.__dict__
                del output_dict[student.username]['userobj']
                del output_dict[student.username]['gl']
            with open(students_file, 'w+') as output:
                json.dump(output_dict, output, indent=2, sort_keys=True)
        self.student_list = parse_students_file(gl, self.course_name)
        for student in self.student_list:
            self.students_by_id[student.id] = student
            self.students[student.username] = student

    def setup(self):
        """Set up this course."""
        gl = self.gl
        options = self.options
        self.group = Group(gl, self.course_name)
        students = self.student_list

        self.setup_paths()

        # Add the graders as a member of the cs416 group
        grader_names = options['grader_usernames']
        self.add_graders(grader_names)

        self.master_proj = gl.projects.get(options['master_project_id'])

        self.add_students(students)

    def add_students(self, students):
        """Add the list of students to the course."""
        for student in students:
            self.add_student(student)

    def add_student(self, student):
        """Add a single student to the course."""
        options = self.options
        group = self.group
        graders = self.graders
        gl = self.gl

        self.create_student_directory(student.username)
        user = student.userobj
        user_group = Group(gl, user.username, group)
        user_group.add_member(user, options['subgroup_access'])
        user_proj = self.fork_master_proj(student, user_group)
        self.add_to_student_project(user_proj,
                                    self.instructor,
                                    options['grader_access'])
        for grader in graders:
            user_group.add_member(grader, options['grader_access'])
            self.add_to_student_project(user_proj,
                                        grader,
                                        options['grader_access'])

    def fork_master_proj(self, student, user_group):
        """Fork the master project into the student group."""
        gl = self.gl
        master_proj = self.master_proj
        group = self.group
        namespace = group.name + '/' + student.username
        fork_name = str(group.name +
                        '/' + user_group.name +
                        '/' + 'Masterproject')
        if not user_group.projects.list():
            master_proj.forks.create({'namespace': namespace})
        student_proj = gl.projects.get(fork_name)
        student_proj.visibility = 'private'
        self.add_assignment_hook(student_proj)
        student_proj.save()
        return student_proj

    def add_to_student_project(self, user_proj, user, access_level):
        """Add a user to a students project with the given access_level."""
        if not user_proj.members.list(query=user.username):
            user_proj.members.create({'user_id': user.id,
                                      'access_level': access_level})
        else:
            member = user_proj.members.get(self.instructor.id)
            member.access_level = gitlab.DEVELOPER_ACCESS
            member.save()

    def add_graders(self, grader_names):
        """Add the list of graders to the course."""
        gl = self.gl
        options = self.options
        for grader_name in grader_names:
            grader = gl.users.list(username=grader_name)[0]
            self.graders.append(grader)
            self.group.add_member(grader, options['grader_access'])

    def setup_paths(self):
        """Set up the necessary paths for the course."""
        if not Path(self.dir['course']).exists():
            Path(self.dir['course']).mkdir()

        if not Path(self.dir['assignments']).exists():
            Path(self.dir['assignments']).mkdir()

        if not Path(self.dir['labs']).exists():
            Path(self.dir['labs']).mkdir()

    def assignment_hook_exists(self, student_proj):
        """Return whether or not a hook already exists."""
        hooks = student_proj.hooks.list()
        for hook in hooks:
            url = hook.url
            test_url = url[0:url.rindex('/')+1]
            if (test_url == "http://0.0.0.0:25001/hooks/" and
                    hook.push_events == 1 and
                    hook.tag_push_events == 1):
                return True

        return False

    def add_assignment_hook(self, student_proj):
        """Add an assignment hook to the project."""
        hook_attrs = {
            'url': 'http://0.0.0.0:25001/hooks/'+getpass.getuser(),
            'push_events': 1,
            'tag_push_events': 1
        }
        if not self.assignment_hook_exists(student_proj):
            student_proj.hooks.create(hook_attrs)

    def create_student_directory(self, student_name):
        """Create the students specific directory."""
        if not Path(self.dir['students']).exists():
            Path(self.dir['students']).mkdir()
        add_student_path = self.dir['students'] / student_name
        if not Path(add_student_path).exists():
            Path(add_student_path).mkdir()

    def get_student(self, username=None, sid=None):
        """Return the user object with the supplied username."""
        assert username is not None and sid is not None, \
            "Can only get student by either username or id, not both"
        assert username is None and sid is None, \
            "Need to supply either a username or id to search with"

        if username is not None:
            assert username in self.students, \
                "Username " + username + " not in course"
            return self.students[username]
        if sid is not None:
            assert sid in self.students_by_id, \
                "ID " + sid + " not in course"
        return self.students[username]

    def get_group(self):
        """Return the group associated with this course."""
        return self.group

    def get_sub_groups(self):
        """Return a list of subgroups contained within this courses."""
        return self.group.get_subgroups_as_groups()
