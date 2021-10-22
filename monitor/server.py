# Server
# idea: actively send information to monitor every 30 sec
from socket import *
from datetime import datetime
import psutil
# from . import DU_PATH
import time

# Set PORT IP
HOST = "127.0.0.1"   # means "local host" (The server's hostname or IP address)
PORT = 12000 # The port used by the server
FORMAT = 'utf-8'
SIZE = 2048
s = socket(AF_INET, SOCK_DGRAM)
connected = True
while connected:
    message = str(datetime.now().timestamp()) + " " + str(psutil.cpu_percent()) + " " + \
    str(psutil.virtual_memory().percent) + " " + str(psutil.disk_usage('.').percent)+ " " + str(psutil.net_io_counters().packets_recv) + " 1"
    s.sendto(message.encode(FORMAT), (HOST, PORT))
    time.sleep(3)
    