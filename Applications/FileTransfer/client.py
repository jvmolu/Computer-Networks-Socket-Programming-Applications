import socket
import sys

s = socket.socket()

serverIP = sys.argv[1]
serverPort = int(sys.argv[2])

s.connect((serverIP, serverPort))

# Authenticating with server
s.send("SECRET_KEY".encode())
# Recieve Authentication Result
data = s.recv(1024)

# If Authentication is not successful
if data == b'AUTH_ERROR':
    print("Authentication Error")
    print("Exiting...")
    s.close()
    exit()
 
# Authentication Successful
print('receiving data...')
 
# Creating a new file named RECIEVED_FILE.txt
with open('RECIEVED_FILE.txt', 'wb') as f:
   
    print('Opened a new file and copying data from server')
   
    while True:
       
        # Receiving data from server
        data = s.recv(1024)
        print('Recieved Data : ', repr(data))
       
        # File Transfer is complete
        if not data:
            break
       
        # Writing data to file
        f.write(data)
 
print('Successfully got the file')
print('Exiting..')
s.close()
print('connection closed')