# Rubber-Ducky Wifi and Chrome Dump
https://github.com/cubidalsphere/Rubber-Ducky
This process is designed to disable windows defender, then copy the wifi information with passwords in clear text into a new directory. Then the stored chrome passwords, and browsing history are dumped into this directory. All files within this directory are emailed to your gmail account.

# wifi passwords
This process is similar to that used by Luca Grosshennig in Payload - Wifi Key grabber, maintaing the use of making the new "l" directory, changing to it and then extracting the wifi accesspoint information to this location.

# Chrome Dump
This is a powersploit by Empire Project, with the raw available at (https://raw.githubusercontent.com/EmpireProject/Empire/master/data/module_source/collection/Get-ChromeDump.ps1).
You will need to modify the output to be in the newly created "l" directory, as this will be added to the email. as this is a .ps1 file you may be able to host this powersploit on a free service such as 000webhost or similar. For ease of execution, you may wish to get a bit.ly / tiny.url or similar that points to your script.

# Email.ps1

You will need to substitute your email and password where it is stated. This script will email all the files that are in the new folder "l" in a single email. this will include all the stored wifi access point information, and the information obtained from "Chrome Dump". If you did not wish to waste time with displaying the names of folders, or that the email has been sent successfully, remove these from the script.
This script can also be hosted on a fee service.
You you may need to adjust your security settings to allow less secure apps.
