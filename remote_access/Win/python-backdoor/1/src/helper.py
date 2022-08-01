"""
https://github.com/xp4xbox/Python-Backdoor

@author    xp4xbox

license: https://github.com/xp4xbox/Python-Backdoor/blob/master/license
"""
import os.path
import sys


# function to return string with quotes removed
def remove_quotes(string): return string.replace("\"", "")


def init_submodule(submodule):
    sys.path.append(f"submodule/{submodule}")


def get_submodule_path(submodule):
    return f"{os.path.dirname(__file__)}/submodule/{submodule}"


# function to return title centered around string
def center(string, title): return f"{{:^{len(string)}}}".format(title)


# function to decode bytes
def decode(data):
    try:
        return data.decode()
    except UnicodeDecodeError:
        try:
            return data.decode("cp437")
        except UnicodeDecodeError:
            return data.decode(errors="replace")
