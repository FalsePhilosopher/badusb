"""
https://github.com/xp4xbox/Python-Backdoor

@author    xp4xbox

license: https://github.com/xp4xbox/Python-Backdoor/blob/master/license
"""
from src.client.persistence.persistence import Persistence


class Unix(Persistence):
    def melt(self):
        raise NotImplementedError

    def detect_vm(self):
        raise NotImplementedError

    def detect_sandboxie(self):
        raise NotImplementedError

    def remove_from_startup(self):
        raise NotImplementedError

    def add_startup(self):
        raise NotImplementedError
