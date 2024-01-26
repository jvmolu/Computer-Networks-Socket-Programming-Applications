import socket
import sys

# Command line arguments
host=sys.argv[1]
port=sys.argv[2]

# Checking the address information
addr_info = socket.getaddrinfo(host, int(port))

# Host and Port
host = addr_info[0][4][0]
port = int(addr_info[0][4][1])

# Address Family
family = addr_info[0][0]

# Socket Type
TCP_TYPE = socket.SOCK_STREAM

# Create a TCP socket
s = socket.socket(family=family, type=TCP_TYPE)

# Bind the socket to the address
s.bind((host, port))

# Listen for incoming connections
s.listen(5)
print("Server is listening on {}:{}".format(host, port))

while(True):
    
    # Accept a connection
    conn, addr = s.accept()
    print('Got a connection from the address : ', addr)
    
    # Communicate with the client
    with conn:
        while True:
            # Receive data from the client
            data = conn.recv(1024)
            print('Recieved Message: ' + data.decode('utf-8'))

            if not data or data.decode('utf-8') == 'exit':
                print('Closing Connection')
                break
            
            # Send data to the client
            print('Sending Acknowledgement')
            conn.sendall("Acknowledgement".encode('utf-8'))
