import datetime
import math
import matplotlib.pyplot as plt
import numpy as np
import socket
import time
import argparse

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

# Function to plot the graph
def plot(X, Y_throughput, Y_delay):

    # Create a Subplot for Throughput and Interval
    plt.subplot(1, 2, 1)
    plt.scatter(X, Y_throughput, c='#cf0412', marker='*', s=70, zorder=10)
    plt.plot(X, Y_throughput, c='#f72533', zorder=5)
    plt.xlabel('Time (in sec)')
    plt.ylabel('Average Throughput (bits/sec)')
    plt.title('Average Throughput (bits/sec)')
    plt.grid(True, zorder=0)
    plt.xticks(np.arange(min(X), max(X)+1, 1.0))
    
    # Create a Subplot for Delay and Interval
    plt.subplot(1, 2, 2)
    plt.scatter(X, Y_delay, c='#0505a6', marker='*', s=70, zorder=10)
    plt.plot(X, Y_delay, c='#2525f7', zorder=5)
    plt.xlabel('Time (in sec)')
    plt.ylabel('Average Delay (in sec)')
    plt.title('Average Delay (in sec)')
    plt.grid(True, zorder=0)
    plt.xticks(range(min(X), max(X)+1, 1))
    
    # Show the graph
    plt.show()

msgFromClient       = "Hello Server."
bytesToSend         = str.encode(msgFromClient)
serverAddressPort   = (serverIP, serverPort)

# Adjusting the buffer size
bufferSize          = packetSize

# Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Initial Timeout
UDPClientSocket.settimeout(interval)

tmsgs = numberOfMessages

# Calibration of Buffer Size
calibrationMessage = str.encode(f"C {packetSize}")
print("\nCalibrating Buffer Size...")
UDPClientSocket.sendto(calibrationMessage, serverAddressPort) # Sending message to the server
Acknowledgement = UDPClientSocket.recvfrom(bufferSize) # Receive message from server
print(Acknowledgement[0].decode())
print()


tmsgs = numberOfMessages

messages = {}

# I will use this to get the time relative to the start of the sending process
originalStartTime = datetime.datetime.now().timestamp()

while numberOfMessages > 0:
    
    # set timeout for the next packet
    UDPClientSocket.settimeout(interval)
    
    # send message to server
    numberOfMessages -= 1
    
    # Timestamp1 is the time when i send the packet and timestamp2 is the time when i will recieve the acknowledgement
    messages[tmsgs - numberOfMessages] = {
        "interval" : interval,
        "timestamp1" : -1,
        "timestamp2" : -1
    }
    
    print(f"Sending message {tmsgs - numberOfMessages} of size {packetSize}: ", msgFromClient)

    # Sending time
    timestamp1 = datetime.datetime.now()
    
    # Send the message to the server
    UDPClientSocket.sendto(bytesToSend, serverAddressPort)

    messages[tmsgs - numberOfMessages]["timestamp1"] = timestamp1.timestamp() - originalStartTime
    
    # recieve message from server
    try:
        Acknowledgement = UDPClientSocket.recvfrom(bufferSize)
        timestamp2 = datetime.datetime.now()
        messages[tmsgs - numberOfMessages]["timestamp2"] = timestamp2.timestamp() - originalStartTime
        print("Acknowledgement: ", Acknowledgement[0].decode())
        print()

        # This is also the RTT for this packet
        delay = timestamp2.timestamp() - timestamp1.timestamp()

        print(f"Interval: {interval}")
        print(f"RTT: {delay}\n")

        # Sleeping for the remaining interval
        time.sleep(max(0, interval - delay))
        
        # Update the interval
        interval = 0.95*interval
        
    except socket.timeout:
        # In case of a timeout, timestamp2 will be -1
        print("Timeout, Packet Loss.\n")
        # Update the interval
        interval = 0.95*interval
        # Skip to the next iteration
        continue

interval = 1
UDPClientSocket.settimeout(interval)
# Telling the server that we are done sending and it should stop listening
print("Finished sending, Terminating the connection..")
UDPClientSocket.sendto(str.encode('exit'), serverAddressPort)
msgFromServer = UDPClientSocket.recvfrom(bufferSize)
print("Message from Server {}".format(msgFromServer[0]))

AverageThroughputs = []
AverageDelays = []

# Print all messages
for key in messages.keys():
    
    print(f"Message {key}")
    print(f"Interval: {messages[key]['interval']}")
    print(f"Timestamp1: {messages[key]['timestamp1']}")
    print(f"Timestamp2: {messages[key]['timestamp2']}\n")
    
    # Checking, which 'second' was this message was sent in.
    # Since RTT's are very small, we will consider that the acknowledgement was received at the same second as the message was sent.
    timeSecond = 0
    if messages[key]['timestamp1'] != int(messages[key]['timestamp1']):
        timeSecond = math.ceil(messages[key]['timestamp1'])
    else:
        timeSecond = int(messages[key]['timestamp1'] + 1)
    
    # Second, in which no message was sent, will have average throughput of 0 and average delay of 0
    while(len(AverageThroughputs) < timeSecond):
        AverageThroughputs.append(0)
        # Delays will be stored in the form [total delay, number of packets]
        AverageDelays.append([0, 0])
    
    # If the packet was not lost and acknowlegement was recieved, then we will calculate the throughput and delay for this message.
    if(messages[key]['timestamp2'] != -1):
        # Multiply by 2 since packet was sent from client to server and then from server to client
        AverageThroughputs[timeSecond-1] += packetSize * 8 * 2
        AverageDelays[timeSecond-1][0] += messages[key]['timestamp2'] - messages[key]['timestamp1']
        AverageDelays[timeSecond-1][1] += 1

# These will be used to plot the graph
X = []
Y_throughput = []
Y_delay = []

# Print average throughput and delay
for second in range(len(AverageThroughputs)):
    print(f"Average Throughput for second {second + 1}: {AverageThroughputs[second]}")
    
    X.append(second+1)
    Y_throughput.append(AverageThroughputs[second])
    
    if(AverageDelays[second][1] != 0):
        print(f"Average Delay for second {second + 1}: {AverageDelays[second][0] / AverageDelays[second][1]}\n")
        Y_delay.append(AverageDelays[second][0] / AverageDelays[second][1])
    else :
        print(f"Average Delay for second {second + 1}: {AverageDelays[second][0]}\n")
        Y_delay.append(AverageDelays[second][0])

# Plot the graph
plot(X, Y_throughput, Y_delay)
