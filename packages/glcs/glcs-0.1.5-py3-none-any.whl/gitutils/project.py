import gitlab
import sys
from student import Student

class ProjectManager:

    def __init__(self, gl):
        self.gl = gl
        ProjectManager.gitlab_instance = gl

    def get(self, id=None):
        pass

    def list(self, archived=None, visbility=None, owned=None, starred=None, search=None):
        pass

    def create(self, settings=None):
        pass

    def delete(self, id=None):
        pass

    def importProject(self, file=None, name=None):
        pass

class Project:

    def __init__(self, gl):
        self.gl = gl

    def snippets(self, enabled=None):
        pass

    def enableSnippets(self):
        pass

    def disableSnippets(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass

    def createFork(self, options=None):
        pass

    def listForks(self):
        pass

    def usedLanguages(self):
        pass

    def star(self):
        pass

    def unstar(self):
        pass

    def archive(self):
        pass

    def unarchive(self):
        pass

    def housekeeping(self):
        pass

    def repoTree(self, path=None, ref=None):
        pass

    def repoBlob(self, forItem=None):
        pass

    def repoArchive(self, sha=None):
        pass

    def snapshot(self):
        pass

    def compareBranches(self, b1=None, b2=None):
        pass

    def compareTags(self, t1=None, t2=None):
        pass

    def compareCommits(self, c1=None, c2=None):
        pass

    def contributors(self):
        pass

    def listUsers(self, search=None):
        pass

    def export(self, options):
        pass
