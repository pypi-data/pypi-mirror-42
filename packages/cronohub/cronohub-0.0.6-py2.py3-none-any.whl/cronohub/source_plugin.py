from abc import ABCMeta, abstractmethod


class CronohubSourcePlugin(metaclass=ABCMeta):
    """
    This is the basic definition of a CronoHub plugin.
    """
    @abstractmethod
    def validate(self):
        ...

    @abstractmethod
    def help(self):
        ...

    @abstractmethod
    def fetch(self):
        """
        Returns a tuple (str, str) where there first parameter is the name of the
        archive and the second is the location as a full path. Exp:
        ("my-project-12345", "/home/user/projects/my-project/my-project.tar.gz")
        """
        ...
