import socket
import sys

# IP at which the server will be listening for calls
localIP     = "0.0.0.0"
publicIP   = socket.gethostbyname(socket.gethostname())

# Port at which the server will be listening for calls
localPort   = int(sys.argv[1])
bufferSize  = 1024

# Acknowledgement Message
SuccessMessage  = "200, UDP Packet Sent Successfully"

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))

# Prining the server details
print(f"UDP server up and listening on address {publicIP} / {localPort}")

# Server Hostname
hostname = socket.gethostname()
print(f"Hostname: {hostname}\n")

# Listen for incoming datagrams
while(True):

    # Receive the client packet along with the address it is coming from
    message, address = UDPServerSocket.recvfrom(bufferSize)
    print(f"Message: {message.decode()}")
    print(f"Address: {address}")
    message = message.decode()

    # Expected Format-> to : <destination IP> / <destination Port> ; content : <message>
    
    # Check if the message is in the expected format
    
    if message.lower() == 'hii':
        UDPServerSocket.sendto(str(address).encode(), address)
        continue
    
    if message == 'exit server':
        break
    
    if(message.count(';') == 0):
        # Send Error Message
        UDPServerSocket.sendto("400".encode(), address)
        continue
    
    colonIndex = message.index(';')
    header = message[:colonIndex]
    data = message[colonIndex+1:]
    
    if(header.count(':') != 1 or header.count('/') != 1 or data.count(':') != 1):
        # Send Error Message
        UDPServerSocket.sendto("401".encode(), address)
        continue
    
    # Destructuring the header
    header = header.split(':')
    To = header[0]
    targetIP, targetPort = header[1].split('/')
    
    if(To.strip().lower() != 'to'):
        # Send Error Message
        UDPServerSocket.sendto("402".encode(), address)
        continue
    
    # strip targetIP and targetPort
    targetIP = targetIP.strip()
    try:
        targetPort = int(targetPort.strip())
    except:
        # Send Error Message
        UDPServerSocket.sendto("403".encode(), address)
        continue
    
    # Header is valid

    if data.split(':')[0].strip().lower() != 'content':
        # Send Error Message
        UDPServerSocket.sendto("404".encode(), address)
        continue
    
    message = data.split(':')[1].strip()
    
    # Data is valid
    
    # Send message to (target IP, target Port)
    try:
        # Put message in format : <source IP> / <source port> ; content : <message>
        UDPServerSocket.sendto(f"{address[0]}/{address[1]} ; content : {message}".encode(), (targetIP, targetPort))
    except Exception as e:
        # Send Error Message
        UDPServerSocket.sendto("405, Could not send the message to the requested address".encode(), address)
        continue
    
    # Send Success Message
    UDPServerSocket.sendto(SuccessMessage.encode(), address)


# Close the server socket
UDPServerSocket.close()
