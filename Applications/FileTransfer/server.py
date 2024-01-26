import socket
import sys

localIP = '0.0.0.0'
publicIP = socket.gethostbyname(socket.gethostname())

port = int(sys.argv[1])

s = socket.socket()
s.bind((localIP, port))

filename = input('Enter the file path: ')

# opening the file
try:
    f = open(filename,'rb')
except:
    print('Please make sure you have entered the correct path')
    exit()

# Listening for the incoming connections
s.listen(1)
print(f'Server running at {publicIP}/{port}')
 
conn, addr = s.accept()
print('Got a new connection from', addr)

# receive authentication key
data = conn.recv(1024)
print('Received Data : ', repr(data))

if data != b'SECRET_KEY':
   conn.send(b'AUTH_ERROR')
   print('closing server')
   conn.close()
   exit()
else:
   conn.send(b'AUTH_SUCCESS')
 
print('Sending file...')

l = f.read(1024) # reading file in chunks

while (l):
   conn.send(l)
   print(f'Sent {1024} units of data')
   l = f.read(1024)
 
# Closing the file
f.close()

print('File sent successfully')
conn.close()
print('Connection closed')