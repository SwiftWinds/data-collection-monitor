# Server
# idea: actively send information to monitor every 30 sec
from socket import *
from datetime import datetime
import psutil
# from . import DU_PATH
import time

# Set PORT IP
HOST = "0.0.0.0"   # means "local host" (The server's hostname or IP address)
PORT = 12000 # The port used by the server
FORMAT = 'utf-8'
SIZE = 2048
device_num = 1
# need to be manually changed

s = socket(AF_INET, SOCK_DGRAM)
#initalize socket


message = "connected"   # send a connected message so monitor can know how many devices are sending info
s.sendto(message.encode(FORMAT), (HOST, PORT))
while True:
    message = str(datetime.now().timestamp()) + " " + str(psutil.cpu_percent()) + " " + \
    str(psutil.virtual_memory().percent) + " " + str(psutil.disk_usage('.').percent)+ " " + \
    str(psutil.net_io_counters().packets_recv) + " " + str(device_num)
    s.sendto(message.encode(FORMAT), (HOST, PORT))
    # send message to server
    time.sleep(3)
    