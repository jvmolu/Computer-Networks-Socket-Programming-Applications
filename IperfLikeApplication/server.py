import socket
import random
import time
import argparse

# IP at which the server will be listening for calls
localIP     = "0.0.0.0"
publicIP    = socket.gethostbyname(socket.gethostname())

# Take port from command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("-p", "--port", help="Port to listen on", type=int, default=8080)
args = parser.parse_args()

# Port at which the server will be listening for calls
localPort   = int(args.port)

bufferSize  = 1024

# Acknowledgement Message
msgFromServer       = "Packet Acknowledged"

# Encoding the message
bytesToSend         = str.encode(msgFromServer)

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
    
    # Receive message from client
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    
    # Destructuring the packet
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]
    
    # Printing the message and address of the client
    print("Message from Client:{}".format(message))
    print("Client Address:{}".format(address))
    print()
    
    # Decoding the message
    decodedMessage = message.decode()
    
    # Checking if the message is for the Calibration of Buffer Size
    # This packet cannot be dropped
    if(decodedMessage[0] == 'C'):
        bufferSize = int(decodedMessage.split()[1])
        UDPServerSocket.sendto(str.encode("Buffer Size Calibrated at Server."), address)
        # Skip to next iteration
        continue
    
    # Checking if the message is for stopping the server
    # This packet cannot be dropped
    if (message == b'exit'):
        UDPServerSocket.sendto(str.encode("Stopping the Server."), address)
        print("Exiting")
        break

    # Artificial delay
    delay = random.randint(1,5000)
    time.sleep(delay/10000)
    
    # random packet drop with a probability of ~0.1
    num = random.randint(1,10)
    if(num <= 1):
        # Skip to next iteration
        continue
    
    # Sending the acknowledgement back to the client
    UDPServerSocket.sendto(bytesToSend, address)

# Close the server socket
UDPServerSocket.close()
