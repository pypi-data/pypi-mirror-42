# -*- coding: utf-8 -*-
"""GroupManager and Group class."""
from .utils import kwargs_to_dict


class GroupManager:
    """Handles common Group manipulation tasks like retrieving, searching, and
    deleting of groups.
    """

    def __init__(self, gl):
        """Pass the gitlab instance to the GroupManager instance."""
        self.gl = gl

    def get_or_create(self, **search_criteria):
        """Return the group, or create it and return it."""
        return self.get(search_criteria)

    def create(self, **groupattrs):
        """Return the group if it could be created, returns None otherwise."""
        pass

    def delete(self, groupname):
        """Return true if the group was deleted, false otherwise."""
        pass

    def group_exists(self, name=None, id=None, parent=None):
        """Return whether the group with the given name exists."""
        pass

    def get(self, **search_criteria):
        """Return the group with the given name, or Not Found"""
        assert (self.gl is not None), \
            "Need a configuration file in order to get a group"
        assert search_criteria is not dict(), \
            "Need to supply a dictionary containing search criteria"

        search_criteria = kwargs_to_dict(search_criteria)

        group = None
        if 'id' in search_criteria:
            group = self.gl.groups.get(search_criteria['id'])
        if 'name' in search_criteria:
            if group is None:
                group = self.gl.groups.list(search=search_criteria['name'])
                if group:
                    group = group[0]
                else:
                    group = None
            elif group.name != search_criteria['name']:
                group = None
        if 'parent_id' in search_criteria:
            if group is not None:
                if group.parent_id != search_criteria['parent_id']:
                    group = None

        return group


class Group:
    """Handles common functions on a python-gitlab group object."""

    def __init__(self, gl, groupname, parentgroup=None):
        """Get or create a group with the supplied name and parent."""
        self.groupmanager = GroupManager(gl)
        groupmanager = self.groupmanager
        group = None
        if parentgroup is None:
            group = groupmanager.get(name=groupname)
            if group is None:
                groupattrs = {
                    'name': groupname,
                    'path': groupname
                }
                group = gl.groups.create(groupattrs)
        else:
            parentgroup = groupmanager.get(name=parentgroup.name)
            subgroups = parentgroup.subgroups.list()
            found = False
            for subgroup in subgroups:
                if subgroup.name == groupname:
                    group = groupmanager.get(id=subgroup.id)
                    found = True
                if found:
                    break

            if not found:
                groupattrs = {
                    'name': groupname,
                    'path': groupname,
                    'parent_id': parentgroup.id
                }
                group = gl.groups.create(groupattrs)

        # define instance variables
        self.parent = parentgroup
        self.name = groupname
        self.group = group
        self.members = {}
        self.id = group.id
        self.projects = group.projects
        self.subgroups = group.subgroups.list()
        # populate group member dictionary for easy member access by username
        mem = group.members.list()
        for member in mem:
            self.members[member.id] = member

    def list_members(self):
        """Return the list of members in the group."""
        return self.group.members.list()

    def get_member(self, memberid):
        """Return the group member with the given id, or None if not found."""
        return self.group.members.get(memberid)

    def is_member(self, member):
        """Return True if member exists, False otherwise."""
        if member.id in self.members:
            return True
        return False

    def add_member(self, user, access):
        """Return True member can be added, False if already a member."""
        if self.is_member(user):
            return False
        member = self.group.members.create({'user_id': user.id,
                                            'access_level': access})
        self.members[member.id] = member
        return True

    def remove_member(self, user):
        """Return False if the member couldn't be removed, else True."""
        if not self.is_member(user):
            return False
        self.group.members.delete(user.id)
        return True

    def get_name(self):
        """Return the name of the current group."""
        return self.group.name

    def list_subgroups(self):
        """Return the subgroups of the group."""
        return self.subgroups

    def get_subgroups_as_groups(self):
        """Get the list of subgroups as Group objects (not SubGroup)."""
        realsubgroups = []
        for subgroup in self.subgroups:
            group = self.groupmanager.get(id=subgroup.id)
            realsubgroups.append(group)
        return realsubgroups
