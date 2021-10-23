# monitor
# idea: listen to the input and put it into database
from datetime import datetime
from socket import *


PORT = 12000
SERVER = "0.0.0.0" # for local network
FORMAT = 'utf-8'
SIZE = 2048

#initalize socket
s = socket(AF_INET, SOCK_DGRAM) 

#bind socket to port and connect
s.bind((SERVER, PORT))

connected = True
connected_device = 0
while connected:
    message, clientAddress = s.recvfrom(SIZE)
    if message:
        decoded_mess = message.decode(FORMAT)

    if decoded_mess == "connected":
        connected_device = connected_device + 1
        print("A new device started sending information")
        continue
        

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
    
