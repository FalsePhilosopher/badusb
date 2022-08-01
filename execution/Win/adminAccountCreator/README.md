# BadUSB_adminAccountCreator
https://github.com/tuconnaisyouknow/BadUSB_adminAccountCreator
# Warning ⚠️
Everything in this repository is **strictly** for educational purposes. Notice **I am not responsible** for stolen data. **You are responsible** for your actions using developed script for **BadUSB**.
# About ℹ️
This **script** allows you to do all this :
* Create a hidden admin account
* Set interactive logon on : "Don't display last signed-in" to allow you to connect to the hidden account
### NB n°1 (for arduino BadUSB)
Sometimes, you will see something like this : 
``` 
Keyboard.press(KEY_LEFT_CTRL);
Keyboard.press(KEY_LEFT_ALT);
Keyboard.press(173);
Keyboard.releaseAll(); 
```
This is only to write these characters : "@", "\\". But it depends on the computer's layout, so adapt these characters thanks to this [site](https://www.csee.umbc.edu/portal/help/theory/ascii.txt) and the sequence you actually use to wirte these characters with your keyboard. (or switch the keyboard layout to French).
### US Layout
For US layout you only have to replace by this for "\\" :
```
Keyboard.press(92);
Keyboard.releaseAll();
```
And by this for "@" :
```
Keyboard.press(64);
Keyboard.releaseAll();
```
### NB n°2
You can customize the **delay** according to the speed in which you plug the **BadUSB**.
### NB n°3
When you plug the BadUSB in a PC you  have to wait for the caps lock to flash to unplug it.
# Getting Started ✔️
## Requirments
1. Have a **BadUSB**.

2. Install **Arduino software** [here](https://www.arduino.cc/en/software) (if you have a BadUSB based on Arduino);

3. Have a victim with **Windows OS** installed in his PC.
## Install
1. Download this repository;

**Linux :**
```
git clone https://github.com/tuconnaisyouknow/BadUSB_keyloggerInjector
cd BadUSB_keyloggerInjector
```
**Windows :** Click on green button on right top of main page. Then click on "Download Zip" and extract zip file.

2. You can edit the name and password of the hidden account [here](https://github.com/tuconnaisyouknow/BadUSB_adminAccountCreator/blob/main/BadUSB_adminAccountCreator.ino) at line 56 or [here](https://github.com/tuconnaisyouknow/BadUSB_adminAccountCreator/blob/main/BadUSB_adminAccountCreator.txt) at line 19;

3. Put the .ino or .txt file in your BadUSB;

4. Find a victim and enjoy !
## Requirments for victim PC
* Turn off caps lock.
* Switch the keyboard layout to French (or adapt the code according to your layout).
