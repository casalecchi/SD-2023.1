import socket
from time import sleep
from datetime import datetime
import os
import sys
from utils import *


COORD_ADDR = ("localhost", 8000)
MESSAGE_SIZE = 10
PID = os.getpid()

def client_process(r, k): 
    for i in range(r):
        # connect to coordinator
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(COORD_ADDR)

        # create, encode and send request message to coordinator
        request_message = create_request_message(PID, MESSAGE_SIZE)
        encoded_request = request_message.encode()
        sock.send(encoded_request)
        
        # wait for grant
        data = sock.recv(MESSAGE_SIZE)
        # close conncetion
        sock.close()

        # decode message received
        decoded_msg = data.decode()
        msg_type, _, _ = decoded_msg.split("|")

        if msg_type == '2':
            # allowed to enter the critical section
            with open("resultado.txt", "a") as file:
                current_time = datetime.now()
                file.write(f"{PID} - {current_time}\n")

            sleep(k)
        
        # connect to coordinator
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(COORD_ADDR)

        # create, encode and send release message
        release_message = create_release_message(PID, MESSAGE_SIZE)
        encoded_release = release_message.encode()
        sock.send(encoded_release)

        # close connection
        sock.close()
        

if __name__ == "__main__":
    inputs = sys.argv
    r, k = map(lambda x: int(x), inputs[1:])
    client_process(r, k)
