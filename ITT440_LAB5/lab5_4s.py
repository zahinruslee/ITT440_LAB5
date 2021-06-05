import socket
import sys
import json
import tqdm
import os

mydata = {"id":"505012", "name":"Azizi", "age":"29"}
sendData = json.dumps(mydata)

# create server socket(TCP socket)
s = socket.socket()
print(f"[+] Socket successfully created")

# the server port
port = 5060

# bind the socket
s.bind(('', port))
print(f"[+] socket binded to " + str(port))

# receive 4096 bytes each time
BUFFER_SIZE = 4096

SEPARATOR = "<SEPARATOR>"

# enabling the server to accept connections
# 5 here is teh number of unaccepted connections  that
# the system will allow before refusing new connections
s.listen(5)
print(f"[+] Socket is listening | Port: {port}")

# accept connections if there is any
client_socket, address = s.accept()

# if below code is executed, that means the sender is connected
print(f"[+] {address} is connected.")

# receive the file infos
# receive using client  socket (not server socket)
received = client_socket.recv(BUFFER_SIZE).decode()
filename, filesize = received.split(SEPARATOR)

# remove absolute path if there is
filename = os.path.basename(filename)

# convert to integer
filesize = int(filesize)

# start receiving the file from teh socket
# and writing to the file stream
progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit = "B", unit_scale = True, unit_divisor = 1024)
with open(filename, "wb") as f:
	for _ in progress:
		# read 1024 bytes from the socket (receive)
		bytes_read = client_socket.recv(BUFFER_SIZE)
		if not bytes_read:
			# nothing is received
			# file trasmitting is done
			print("File received successfully")
			break

		# write to the file the bytes we just received
		f.write(bytes_read)

		# update the progress bar
		progress.update(len(bytes_read))

# close the client socket
client_socket.close()

# close the server socket\
s.close()

#while True:
#	c, addr = s.accept()
#	print("Got connection from " + str(addr))

#	c.sendall(bytes(sendData, encoding = "utf-8"))
#	buffer = c.recv(1024)
#	print(buffer)
#c.close()
