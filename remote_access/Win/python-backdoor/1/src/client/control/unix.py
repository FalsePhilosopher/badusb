"""
https://github.com/xp4xbox/Python-Backdoor
@author    xp4xbox
"""

from src.client.control.control import Control


class Unix(Control):
    def __init__(self, _es):
        super().__init__(_es)

    def inject_shellcode(self, buffer):
        raise NotImplementedError

    def toggle_disable_process(self, process, popup):
        raise NotImplementedError

    def lock(self):
        raise NotImplementedError
