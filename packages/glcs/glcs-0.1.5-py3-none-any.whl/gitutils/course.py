# -*- coding: utf-8 -*-
"""CourseManager and Course classes."""
import sys
import json
import os
import readline  # pylint: disable=E0401,unused-import
from pathlib import Path
from gitlab import Gitlab
import gitlab
import jinja2
from gitutils.student import Student
from gitutils.groups import Group


def tryinput(prompt):
    """Try input() and catch KeyboardInterrupts."""
    try:
        output = input(prompt)
    except KeyboardInterrupt:
        print()
        print("Ctrl+C pressed, exiting")
        sys.exit()
    return output


def parse_roster(roster_file, gl):  # pylint: disable=invalid-name
    """Parse the roster file into a set of Student objects."""
    students = []
    enrolled_list = roster_to_enrolled_list(roster_file)
    for enrolled in enrolled_list:
        # create a student using the line we parsed
        student = Student(gl, enrolled)
        # add the student to the list
        students.append(student)
    return students


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
        self.gl = Gitlab.from_config(server, [conf])  # pylint: disable=invalid-name
        # Make sure the gl.user object exists
        self.gl.auth()
        # Save the current user as the instructor
        # (Assumes its the insctructors config file)
        self.instructor = self.gl.user

    @staticmethod
    def create_course_config(course_name, options_file):
        """Create a course config file with for the given coursename."""
        options = {}
        options['course_name'] = course_name
        options['roster_file'] = tryinput("Roster file path? " +
                                          " (path is relative to ~/) ")
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

        with open(options_file, 'w+') as opt:
            json.dump(options, opt, indent=2, sort_keys=True)
        print("Configuration saved to ", options_file)

        return options

    def setup_course(self, course_name):
        """Create a course from a set of course options and a class rosterfile.

        Runs verifyCourse after course creation.
        """
        gl = self.gl  # pylint: disable=invalid-name
        course_path = Path.home() / 'courses'
        if not Path(course_path).exists():
            Path(course_path).mkdir()
        config_path = Path.home() / 'courses' / (course_name+'.cfg')
        options = {}
        if Path(config_path).exists():
            print("Saved course configuration found: ", config_path)
            reuse = ''
            while (reuse.lower() != 'y' and reuse.lower() != 'n'):
                reuse = tryinput("Would you like to reuse this configuration? \
                                    (Y/n) ")
            if reuse.lower() == 'y':
                with open(config_path) as opts:
                    options = json.load(opts)
            else:
                options = self.create_course_config(course_name, config_path)
        else:
            print("No configuration file found for course", course_name)
            options = self.create_course_config(course_name, config_path)

        # Parse the roster file and get a list of students
        options['instructor'] = self.instructor
        course = Course(options, gl)
        course.setup()
        self.verifyCourse(course_name)

    def verifyCourse(self, coursename):
        """Verifies that a course that was created was set up with the proper
        settings and users.
        """
        # Parse through the options file
        configpath = Path.home() / 'courses' / (coursename+'.cfg')
        gl = self.gl
        assert (Path(configpath).exists()), \
            "Could not find course configuration file for course " + coursename
        with open(configpath) as configfile:
            options = json.load(configfile)
        roster_file = options["roster_file"]
        className = options["course_name"]
        project_id = options["master_project_id"]
        masterproj = gl.projects.get(project_id)
        project_name = masterproj.name
        access_level_conv = { 10:"GUEST_ACCESS", 20:"REPORTER_ACCESS",
        30:"DEVELOPER_ACCESS", 40:"MAINTAINER_ACCESS", 50:"OWNER_ACCESS" }

        group = Group(gl, className)

        # Parse the roster file and get a list of students
        options['instructor'] = self.instructor
        classlist = Course(options, gl)
        students = classlist.student_list

        # Grab the subgroups in the group
        subgroups = group.listSubgroups()
        output_list = []

        incorrect_student_settings = 0
        correct_student_settings = 0

        errorLog = []
        userNameList = []
        for student in students:
            userNameList.append(student.username)
        # Check if list of students is in the group
        for student in students:
            output_dictionary = {"Username" : "",
                                 "Project" : "", "Sub_group_access" : "",
                                 "Visibility" : "", "Graders" : {},
                                 "incorrect_settings" : "", "correct_settings" : ""}
            userID = student.id
            name = student.username
            output_dictionary["Username"] = name
            isMember = False
            # Go through each subgroup and match with each user to get info
            for sub in subgroups:
                if( sub.name not in userNameList ):
                    if( sub.name + " has an account in gitlab but isn't in the roster" not in errorLog ):
                        incorrect_student_settings = incorrect_student_settings + 1;
                        errorLog.append(sub.name + " has an account in gitlab but isn't in the roster")
                if(sub.name == name):
                    isMember = True
                    real_group = gl.groups.get(sub.id)
                    visibility = sub.visibility
                    project = real_group.search('projects', project_name)
                    path = project[0]['path_with_namespace']
                    sub_mem = real_group.members.list()
                    print(sub_mem)
                    for mem in sub_mem:
                        if(mem.username == name):
                            sub_access = mem.access_level
                            if( sub_access == options['subgroup_access'] ):
                                output_dictionary["Sub_group_access"] = str(access_level_conv[sub_access])
                            else:
                                output_dictionary["Sub_group_access"] = "NOT " + str(access_level_conv[options["subgroup_access"]])
                                output_dictionary["incorrect_settings"] = True
                        else:
                            for graders in options["grader_usernames"]:
                                if( mem.username not in options["grader_usernames"] and mem.access_level == options['grader_access'] ):
                                    if( name + " has unnecessary grader, " + mem.username not in errorLog):
                                        errorLog.append(name + " has unnecessary grader, " + mem.username)
                                if( graders == mem.username ):
                                    print("Right grader " + str(mem.username))
                                    grader_name = mem.username
                                    grader_sub_access = mem.access_level

                                    # Check access level of grader
                                    if( grader_sub_access == options['grader_access']):
                                        output_dictionary["Graders"][grader_name] = str(access_level_conv[grader_sub_access])
                                    else:
                                        output_dictionary["Graders"][grader_name] = str(access_level_conv[grader_sub_access])
                                        output_dictionary["incorrect_settings"] = True
                                else:
                                    print("Not a grader: " + str(mem.username))
                                    print("Expected grader: " + str(graders))

                    if( len(output_dictionary["Graders"]) == 0 and len(options['grader_usernames']) > 0 ):
                        output_dictionary["Graders"] = "None"
                        output_dictionary["incorrect_settings"] = True

                    # Check if user has visibility set to private
                    if( visibility == 'private'):
                        output_dictionary["Visibility"] = str(visibility)
                    else:
                        output_dictionary["Visibility"] = str(visibility)
                        output_dictionary["incorrect_settings"] = True

                    # Check if user has projects in their subgroup
                    expected_path = options['course_name'] + "/" + student.username + "/" + project_name
                    if( path.lower() == expected_path.lower() ):
                        output_dictionary["Project"] = project_name
                    else:
                        output_dictionary["Project"] = "NOT " + project_name
                        output_dictionary["incorrect_settings"] = True

            if( isMember == False ):
                print("isMember")
                notMember = name + " is in the roster file but doesn't have an account in gitlab"
                errorLog.append(notMember)

            for graders in options["grader_usernames"]:
                if( graders not in output_dictionary["Graders"] ):
                    print("missing grader: " + str(graders))
                    output_dictionary["incorrect_settings"] = True

            for g in options["grader_usernames"]:
                print("g: " + g + " , " + str(output_dictionary["Graders"]))
                print("bool: " + str(g in output_dictionary["Graders"]))
                if( g in output_dictionary["Graders"] == False):
                    print("yes " + g)
                else:
                    print("no")

            if( output_dictionary["incorrect_settings"] == "" ):
                output_dictionary["correct_settings"] = True
                output_dictionary["incorrect_settings"] = False
                correct_student_settings = correct_student_settings + 1;
            else:
                output_dictionary["correct_settings"] = False
                incorrect_student_settings = incorrect_student_settings + 1;
            output_list.append(output_dictionary)

        print(output_list)

        print("options: " + str(options))
        render_vars = { "expected": options, "users": output_list,
        "incorrect_settings": incorrect_student_settings,
        "correct_settings": correct_student_settings, "expected_project": project_name,
        "expected_sub_access": access_level_conv[options['subgroup_access']],
        "expected_grader_access":access_level_conv[options['grader_access']],
        "errorLog": errorLog }

        script_path = os.path.dirname(os.path.realpath(__file__))
        home_path = str(Path.home())
        template_file_location = os.path.join(script_path, 'templates')
        if(Path(template_file_location).exists()):
            print(template_file_location)
        template_file_path = os.path.join(template_file_location, 'verify_output.html')
        rendered_file_path = os.path.join(home_path, coursename+"-setup-results.html")

        environment = jinja2.Environment(loader=jinja2.FileSystemLoader(template_file_location))
        output_text = environment.get_template('verify_output.html').render(render_vars)
        with open(rendered_file_path, "w+") as result_file:
            result_file.write(output_text)


class Course:
    """Handles Course-wide functions and data."""

    def __init__(self, options, gl):
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
        self.gl = gl  # pylint: disable=invalid-name
        self.course_dir = Path.home() / 'courses' / self.course_name
        self.students_dir = self.course_dir / 'students'
        self.assignments_dir = self.course_dir / 'assignments'
        self.labs_dir = self.course_dir / 'labs'

        students_file = self.students_dir / 'students.json'
        if not Path(students_file).exists():
            self.student_list = parse_roster(options['roster_file'], gl)
            output_dict = {}
            for student in self.student_list:
                output_dict[student.username] = student.__dict__
                del output_dict[student.username]['userobj']
                del output_dict[student.username]['gl']
            with open(students_file, 'w+') as output:
                json.dump(output_dict, output, indent=2, sort_keys=True)
        with open(students_file) as opts:
            self.students = json.load(opts)
        for student in self.students:
            student = Student(gl, from_dict=self.students[student])
            self.student_list.append(student)
            self.students_by_id[student.id] = student
            self.students[student.username] = student

    def setup(self):
        """Set up this course."""
        gl = self.gl  # pylint: disable=invalid-name
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
        gl = self.gl  # pylint: disable=invalid-name

        self.create_student_directory(student.username)
        user = student.userobj
        user_group = Group(gl, user.username, group)
        user_group.addMember(user, options['subgroup_access'])
        user_proj = self.fork_master_proj(student, user_group)
        self.add_to_student_project(user_proj,
                                    self.instructor,
                                    options['grader_access'])
        for grader in graders:
            user_group.addMember(grader, options['grader_access'])
            self.add_to_student_project(user_proj,
                                        grader,
                                        options['grader_access'])

    def fork_master_proj(self, student, user_group):
        """Fork the master project into the student group."""
        gl = self.gl  # pylint: disable=invalid-name
        master_proj = self.master_proj
        group = self.group
        namespace = group.getName() + '/' + student.username
        fork_name = str(group.getName() +
                        '/' + user_group.getName() +
                        '/' + 'Masterproject')
        if not user_group.projects.list():
            master_proj.forks.create({'namespace': namespace})
        student_proj = gl.projects.get(fork_name)
        student_proj.visibility = 'private'
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
            self.group.addMember(grader, options['grader_access'])

    def setup_paths(self):
        """Set up the necessary paths for the course."""
        if not Path(self.course_dir).exists():
            Path(self.course_dir).mkdir()

        if not Path(self.assignments_dir).exists():
            Path(self.course_dir).mkdir()

        if not Path(self.labs_dir).exists():
            Path(self.labs_dir).mkdir()

    def create_student_directory(self, student_name):
        """Create the students specific directory."""
        if not Path(self.students_dir).exists():
            Path(self.students_dir).mkdir()
        add_student_path = self.students_dir / student_name
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
        return self.group.getSubgroupsAsGroups()
