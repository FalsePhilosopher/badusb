"""
https://github.com/xp4xbox/Python-Backdoor

@author    xp4xbox
"""
import abc


class Persistence(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def detect_sandboxie(self):
        pass

    @abc.abstractmethod
    def remove_from_startup(self):
        pass

    @abc.abstractmethod
    def add_startup(self):
        pass

    @abc.abstractmethod
    def detect_vm(self):
        pass

    @abc.abstractmethod
    def melt(self):
        pass
