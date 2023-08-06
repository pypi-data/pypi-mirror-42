# -*- coding: utf-8 -*-
"""Student class."""


class Student:
    """Class to encapsulate student details.

    A convenience class that contains a gitlab.User object as well as
    student information gathered from a rosterfile.
    """

    def __init__(self, gl, from_dict=None):
        """Construct a student objectself.

        Take a list of attributes gathered from a rosterfile and assigns
        them to a set of attributes which represents a student. Also gets the
        gitlab.User object for the supplied username within the rosterfile.
        """
        self.gl = gl
        self.from_dict(from_dict)

    def display(self):
        """Output all the attributes of the student."""
        print(self.username)
        print(self.year)
        print(self.month)
        print(self.major)
        print(self.classnum)
        print(self.labnum)
        print(self.lname)
        print(self.fname)
        print(self.mname)
        print(self.email)

    def from_dict(self, student_dict):
        """Populate this student object from a dictionary."""
        gl = self.gl
        self.username = student_dict['username']
        self.userobj = gl.users.list(username=self.username)[0]
        self.id = self.userobj.id
        self.year = student_dict['year']
        self.month = student_dict['month']
        self.major = student_dict['major']
        self.classnum = student_dict['classnum']
        self.labnum = student_dict['labnum']
        self.lname = student_dict['lname']
        self.fname = student_dict['fname']
        self.mname = student_dict['mname']
        self.email = student_dict['email']
