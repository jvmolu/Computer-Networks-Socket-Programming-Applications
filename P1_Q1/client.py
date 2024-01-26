import socket
import time
import datetime
import argparse

# Message to be sent to the server
msgFromClient       = "Hello Server"
bytesToSend         = str.encode(msgFromClient)

# Command line arguments using argparse
parser = argparse.ArgumentParser()
parser.add_argument('-ip' , dest="serverIP", help="IP address of the server", type=str)
parser.add_argument('-port', dest="serverPort", help="Port number of the server", type=int)
parser.add_argument('-n', dest="numberOfMessages", help="Number of messages to be sent", type=int)
parser.add_argument('-i', dest="interval", help="Interval between messages", type=float)
parser.add_argument('-s', dest="packetSize" ,help="Size of the packet", type=int)

args = parser.parse_args()

serverIP            = args.serverIP
serverPort          = int(args.serverPort)
numberOfMessages    = int(args.numberOfMessages)
interval            = float(args.interval)
packetSize          = int(args.packetSize)

# Server Address
serverAddressPort   = (serverIP, serverPort)

# Setting the buffer size
bufferSize          = packetSize

# Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

averageRTT = 0

# Setting Timeout
UDPClientSocket.settimeout(interval)

tmsgs = numberOfMessages
successPackets = 0

# Calibration of Buffer Size
calibrationMessage = str.encode(f"C {packetSize}")
print("\nCalibrating Buffer Size...")
UDPClientSocket.sendto(calibrationMessage, serverAddressPort) # Sending calibration message to the server
Acknowledgement = UDPClientSocket.recvfrom(bufferSize) # Receive acknowledgement message from the server
print(Acknowledgement[0].decode())
print()

# Send to server using created UDP socket
while numberOfMessages > 0:

    numberOfMessages -= 1
    
    print(f"Sending message of {bufferSize} bytes: " + str(tmsgs - numberOfMessages))
    
    timestamp1 = datetime.datetime.now().timestamp()
    
    UDPClientSocket.sendto(bytesToSend, serverAddressPort) # Sending message to the server

    try:
        msgFromServer = UDPClientSocket.recvfrom(bufferSize) # Receive message from server
    except socket.timeout: # If the server does not respond within the timeout period
        print("PACKET LOSS OCCURRED SENDING NEXT PACKET\n")
        continue
    
    timestamp2 = datetime.datetime.now().timestamp()
    
    # Printing the acknowledgement message and the RTT
    print("Message from Server {}".format(msgFromServer[0]))
    print(f"RTT for packet {tmsgs - numberOfMessages}: {timestamp2-timestamp1}\n")

    averageRTT += timestamp2 - timestamp1
    successPackets += 1
    rtt = timestamp2-timestamp1
    
    # Sleep for the remaining interval
    time.sleep(max(interval-rtt, 0))


# Telling the server to stop
print("Finished sending.")
UDPClientSocket.sendto(str.encode('exit'), serverAddressPort)
msgFromServer = UDPClientSocket.recvfrom(bufferSize)
print("Final Message from the Server {}".format(msgFromServer[0]))

# Calculating the average RTT and the loss percentage
lossPackets = (tmsgs - successPackets)
lossPercentage = (lossPackets / tmsgs) * 100
averageRTT /= successPackets

print("Average RTT: {}\n".format(averageRTT))
print("Loss Percentage: {}%\n".format(lossPercentage))

# Close the client socket
UDPClientSocket.close()
