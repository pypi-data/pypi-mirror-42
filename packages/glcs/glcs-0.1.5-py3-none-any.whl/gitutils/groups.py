import gitlab

class GroupManager:
    """Handles common Group manipulation tasks like retrieving, searching, and
    deleting of groups.
    """

    def __init__(self, gl):
        """Captures the gitlab.Gitlab object and sets the class Gitlab instance."""
        self.gl = gl

    def getOrCreate(self, groupname, parent=None):
        """Returns the group if it exists, or creates and returns it if it doesn't."""
        return Group(self.gl, groupname, parentgroup=parent)

    def get(self, groupname, parent=None):
        """Returns the group if it exists, or None otherwise."""
        return Group(self.gl, groupname, parentgroup=parent)

    def create(self, groupname, parent=""):
        """Returns the group if it could be created, returns None otherwise."""
        pass

    def deleteGroup(self, groupname):
        """Returns true if the group was deleted, false otherwise."""
        pass

    def getGroup(self, name=None, id=None):
        """Returns the group with the given name, or Not Found"""
        assert (self.gl != None), \
            "Need a configuration file in order to get a group"
        assert not (name == None and id == None), \
            "Need to supply either name or id keyword argument"
        assert not (name != None and id != None), \
            "Can't supply both name and id keyword argument, only one"

        if(name != None):
            group = self.gl.groups.list(search=name)
            if(len(group) == 0):
                return None
            return group[0]
        if(id != None):
            group = self.gl.groups.get(id)
            return group
        return None

    def searchGroups(self, search_criteria):
        """Returns a list of groups matching the search_criteria, or Not Found"""
        assert (self.gl != None), \
            "Need a configuration file in order to search for a group"
        group = self.gl.groups.list(search=search_criteria)
        if(len(group) == 0):
            return None
        return group


class Group:
    """Handles common functions on a python-gitlab group object."""

    def __init__(self, gl, groupname, parentgroup=None):
        """Gets or creates a group with the supplied name and parent."""
        self.groupmanager = GroupManager(gl)
        groupmanager = self.groupmanager
        group = None
        if(parentgroup == None):
            group = groupmanager.getGroup(name=groupname)
            if(group == None):
                groupattrs = {
                    'name': groupname,
                    'path': groupname
                }
                group = gl.groups.create(groupattrs)
        else:
            parentgroup = groupmanager.getGroup(name=parentgroup.name)
            subgroups = parentgroup.subgroups.list()
            found = False
            for subgroup in subgroups:
                if(subgroup.name == groupname):
                    group = groupmanager.getGroup(id=subgroup.id)
                    found = True;
                if(found):
                    break;

            if(not found):
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

    def listMembers(self):
        """Returns the list of members in the group."""
        return self.group.members.list()

    def getMember(self, memberid):
        """Returns the group member with the given id, or None if not found."""
        return self.group.members.get(memberid)

    def isMember(self, member):
        """Returns True if the supplied members id is in the members dictionary,
        False otherwise.
        """
        if member.id in self.members:
            return True
        return False

    def addMember(self, user, access):
        """Returns True if the supplied username could be added as a member,
        False if the username is already a member.
        """
        if self.isMember(user):
            return False
        member = self.group.members.create({'user_id': user.id, 'access_level': access})
        self.members[member.id] = member
        return True

    def removeMember(self, user):
        """Returns False if the member couldn't be removed, returns True
        otherwise.
        """
        if not self.isMember(user):
            return False
        self.group.members.delete(user.id)
        return True

    def getName(self):
        """Returns the name of the current group."""
        return self.group.name

    def listSubgroups(self):
        """Returns the subgroups of the group"""
        return self.subgroups

    def getSubgroupsAsGroups(self):
        realsubgroups = []
        for subgroup in self.subgroups:
            group = self.groupmanager.getGroup(id=subgroup.id)
            realsubgroups.append(group)
        return realsubgroups
