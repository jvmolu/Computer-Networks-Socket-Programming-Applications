import socket
import sys

# Command line arguments
host=sys.argv[1]
port=sys.argv[2]

# Checking address information
addr_info = socket.getaddrinfo(host, int(port))

# Host and Port
host = addr_info[0][4][0]
port = int(addr_info[0][4][1])

# Address family
family = addr_info[0][0]

# Socket type
TCP_TYPE = socket.SOCK_STREAM

# Create a socket
s = socket.socket(family=family, type=TCP_TYPE)

# Connect to the server
s.connect((host, int(port)))

# Send 5 messages
numberOfMessages = 5
while numberOfMessages > 0:
    numberOfMessages -= 1
    s.sendall("Hii Server".encode('utf-8'))
    Acknowledgement = s.recv(1024)
    print('Acknowledgement Recieved: ' + Acknowledgement.decode('utf-8'))

# Tell the server to stop
s.sendall("exit".encode('utf-8'))

# Close the socket
s.close()
print('Connection closed')
