# monitor
# idea: listen to the input and put it into database
from datetime import datetime
from socket import *

# For this example, we'll use PORT = 12000
PORT = 12000
SERVER = "127.0.0.1"   # means "local host"  only for testing
FORMAT = 'utf-8'
SIZE = 2048

#initalize socket
s = socket(AF_INET, SOCK_DGRAM) 

#bind socket to port and connect
s.bind((SERVER, PORT))

connected = True

while connected:
    message, clientAddress = s.recvfrom(SIZE)
    if message:
        decoded_mess = message.decode(FORMAT)

    if (decoded_mess == "Disconnect"):
            print("Got a disconnect request. Bye.")
            connected = False
            break
        #check connection
        # if(decoded_mess == "Hello"):
        #     responseMessage = "Hiya"
        #     s.sendto(responseMessage.encode(FORMAT), clientAddress)
        #     print("Received this message:", modMessage)

    data_list = [float(x) for x in decoded_mess.split()]
    # split the data into arrays for ez access
    timestamp = data_list[0]
    cpu_used = data_list[1]
    mem_used = data_list[2]
    disk_used = data_list[3]
    total_packets_received_so_far = data_list[4]
    server_num = data_list[5]

    print("time: "+ str(datetime.fromtimestamp(timestamp)))
    print("other data: ", cpu_used, mem_used, disk_used, total_packets_received_so_far, server_num)
    
