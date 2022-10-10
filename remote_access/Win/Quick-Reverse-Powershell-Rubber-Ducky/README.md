## original repo
https://github.com/makozort/Quick-Reverse-Powershell-Rubber-Ducky

# Quick-Reverse-Powershell-Rubber-Ducky

A PEN testing script to demonstrate how quickly a reverse shell can be created with the rubber ducky

THIS SCRIPT IS INTENDED FOR USE ON SYSTEMS YOU OWN OR HAVE BEEN GIVEN PERMISSION TO USE, I TAKE NO RESPONSIBILITIES FOR ANY MISUSE


This script uses netcat, make sure it is ready on on of your machines 

_-How to use-_


Step 1: in rs.ps1,  change {IP HERE} and {PORT HERE} to your ip and port of choosing (you will have to port forward this to the machine you are listening to)

Step 2: either host the file somewhere youself or upload it to a file hosting website, I use anonfiles. (make sure you get the download link, not the page link)

step 3: in ducky.txt, put the link in the "LINK HERE" spot

step 4: encode the payload 

step 5: on your machine with netcat, type the following command: Nc -lnvp {PORT YOU ARE FORWADING TO THIS MACHINE}

step 6: if all goes well, the rubber ducky should start a hidden powershell session that you have full, remote control of a powershell session

some notes: this wont work if they have any anti-virus that isn't windows defender, additionally some networks may block the connection, but it will work on normal home networks ect.

feel free to ask me questions in my dms on twitter @makozort
