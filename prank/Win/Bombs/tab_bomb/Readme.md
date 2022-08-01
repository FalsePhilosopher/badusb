https://github.com/hak5darren/USB-Rubber-Ducky/wiki/Payload---mobiletabs

The following is just something that types in a VB script that sends command line arguments to internet explorer and opens new tabs based on the URLs you specify via command line. 

```
REM AUTHOR: overwraith
REM MOBILETABS.TXT BEGINS
GUI r
STRING cmd /Q /D /T:0a /F:OFF /V:OFF /K
DELAY 500
ENTER
DELAY 750
REM DELETE THE SCRIPT IF IT ALREADY EXISTS
STRING DEL /Q MobileTabs.vbs
ENTER
REM VB SCRIPT FOUND AT:
REM http://www.vistaheads.com/forums/microsoft-public-internetexplorer-general/438407-command-line-open-several-websites-multiple-tabs.htmlinternetexplorer
REM INPUT FILE MobileTabs.vbs
STRING copy con MobileTabs.vbs
ENTER
STRING on error resume next
ENTER
STRING navOpenInBackgroundTab = &h1000
ENTER
STRING set oIE = CreateObject("InternetExplorer.Application")
ENTER
STRING Set args = WScript.Arguments
ENTER
STRING oIE.Navigate2 args.Item(0)
ENTER
STRING for intx = 1 to args.count
ENTER
STRING oIE.Navigate2 args.Item(intx), navOpenInBackgroundTab
ENTER
STRING next
ENTER
STRING oIE.Visible = true
ENTER
CONTROL z
ENTER
REM RUN THE VB SCRIPT TO LAUNCH INTERNET EXPLORER
REM THE DOUBLE QUOTES BECOME MORE IMPORTANT FOR LONGER URLs
STRING MobileTabs.vbs "http://www.google.com/" "http://mwomercs.com/" "http://hak5.org/" "http://forums.hak5.org/index.php?/forum/56-usb-rubber-ducky/"
ENTER
```
