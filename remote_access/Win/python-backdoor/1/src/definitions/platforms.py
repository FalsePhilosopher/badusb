"""
https://github.com/xp4xbox/Python-Backdoor

@author    xp4xbox
"""
import platform

WINDOWS = 0
LINUX = 1
DARWIN = 2
UNKNOWN = -1

UNIX = 3
platform_type = platform.system().lower()
if platform_type == "windows":
    OS = WINDOWS
elif platform_type == "linux":
    OS = LINUX
elif platform_type == "darwin":
    OS = DARWIN
elif platform_type == "":
    OS = UNKNOWN
