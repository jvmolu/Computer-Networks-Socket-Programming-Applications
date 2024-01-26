# Importing the socket library
import socket
import sys

# Server IP address and port number
ip = sys.argv[1]
port = int(sys.argv[2])
myPort = -1
myIP = -1
initialized = False

# Creating a UDP socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def init():
    
    global myIP
    global myPort
    
    # send a hii message to server
    s.sendto("hii".encode(), (ip, port))
    # Receiving the message from the server
    data, address = s.recvfrom(1024)
    
    # decoding data
    print(data.decode())
    data = data.decode()
    data = data[1:-1]

    # extracting IP and Port
    myIP = data.split(",")[0].strip()[1:-1]
    myPort = int(data.split(",")[1].strip())

    # printing the IP and Port
    print(f"My IP is {myIP} and my port is {myPort}")

def send_message():
    
    if not initialized:
        print("Initialize first.")
        return
    
    # recipient address
    recipientIP = input("Enter the recipient's IP address: ")
    recipientPort = int(input("Enter the recipient's port number: "))

    # Sending the message to the server
    message = input("Enter your message: ")

    # Message Format-> to : <recipientIP> / <recipientPort> ; content : <message>

    # Formatting the message
    mymessage = "to:" + recipientIP + "/" + str(recipientPort) + ";content:" + message

    # Sending the message to the server
    s.sendto(mymessage.encode(), (ip, port))

    # Receiving the message from the server
    data, address = s.recvfrom(1024)

    if data.decode().startswith('200'):
        print("Message Sent")
    else:
        print("Message not sent")
        print("Error :", data.decode())

def receive_message():
    
    # Receiving the message from the server
    
    if not initialized:
        print("Initialize first.")
        return
    
    print(f"Waiting for the message at {myIP}/{myPort}...")
    print()
    data, address = s.recvfrom(1024)
    print(f"Message received from {address[0]}/{address[1]}")

    # Printing the message
    print("Message: ", data.decode())

while True:
    print("1. Initialize")
    print("2. Send Message")
    print("3. Receive Message")
    print("4. Exit")
    print("5. Close Server")
    choice = int(input("Enter your choice (1/2/3/4/5): "))
    if choice == 1:
        if initialized:
            print("Already initialized.")
        else:
            init()
            initialized = True
    elif choice == 2:
        if not initialized:
            print("Initialize first.")
        else:
            send_message()
    elif choice == 3:
        if not initialized:
            print("Initialize first.")
        else:
            receive_message()
    elif choice == 4:
        break
    elif choice == 5:
        s.sendto("exit server".encode(), (ip, port))
        break
    else:
        print("Invalid choice.")
