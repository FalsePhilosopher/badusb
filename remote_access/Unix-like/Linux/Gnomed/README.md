# gnomed
https://codeberg.org/chillz/gnomed

### Flipper Zero / Rubber Ducky BadUSB reverse shell targeting Gnome-based Linux distros

A simple script designed for opening a reverse shell on the target linux computer, and setting up rudimentary persistence.<br>
Designed to work on Fedora workstations, but it *should* work on other Gnome-based distributions.<br>
Before testing, make sure you set up a listener and modify the payload accordingly!<br>

### How does this work:
The `ALT+F2` GUI run window is opened. The payload will write the reverse shell script into the `.bashrc` file of the current user. Next, a terminal window is opened for a blink of an eye, to run the freshly added command. This way, every time the terminal is opened on the target, the device will attempt to re-establish the connection, should it be lost. The payload has some nifty tricks that make it unobtrusive for the victim after deployement, to decrease chances of detection.

### How to prevent this type of attacks?
- First of all, remain vigilant about plugging in any USB device into your computer. An attacker can disguise their malware inside of even innocent-looking USB cables, pendrives, keyboards, mice, and other gadgets.
- Lock your computer, when you are away.
- You can consider physically blocking your ports, or hardening your device to not trust new devices right away.

##### This software is public domain. I do not take any responsibility for your actions.
