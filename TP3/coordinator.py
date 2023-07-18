import os
import socket
import threading
from collections import deque
from utils import *


# constants
MESSAGE_SIZE = 10
COORD_ADDR = ("localhost", 8000)

# global variables
close_socket = False
log_file = 'log.txt'
# data structures 
messages_queue = deque()
access_stats = {}
# semaphores
queue_sem = threading.Semaphore(1)
critical_sem = threading.Semaphore(1)
log_sem = threading.Semaphore(1)


# terminal thread
def terminal_interface():
    global close_socket

    while True:
        command = input("Command: ")

        if command == "queue":
            print(messages_queue)
        elif command == "stats":
            print(access_stats)
        elif command == "end":
            close_socket = True
            os._exit(0)
        else:
            print("Invalid input")



# thread to receive messages and create other threads to process them
def receive_messages():
    global close_socket, queue_sem, log_sem

    # create socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(COORD_ADDR)
    sock.listen(socket.SOMAXCONN)

    while not close_socket:
        # waiting for a connection
        client, _ = sock.accept()
        data = client.recv(MESSAGE_SIZE)

        # put message on queue and write on log
        queue_sem.acquire()
        log_sem.acquire()

        write_to_log(data, log_file)
        messages_queue.append(data)
        
        log_sem.release()
        queue_sem.release()

        # create new thread to process new message
        process_thread = threading.Thread(target=process_request, args=(client,))
        process_thread.start()

    sock.close()


# thread to process messages
def process_request(client: socket):
    global log_sem, queue_sem, critical_sem

    # read the next message on queue
    queue_sem.acquire()
    next_message = messages_queue.popleft()
    queue_sem.release()

    message_type, pid = decode_message(next_message)

    # process the REQUEST message
    if message_type == 1:
        # create the permission message
        grant_message = create_grant_message(pid, MESSAGE_SIZE)
        data = grant_message.encode()

        # enter critical section and send permission to client
        critical_sem.acquire()

        # write grant permission on log
        log_sem.acquire()
        write_to_log(data, log_file)
        log_sem.release()

        client.send(data)

    # process the RELEASE message
    if message_type == 3:
        # compute statistics
        access_stats[pid] = access_stats.get(pid, 0) + 1
        # free critical section
        critical_sem.release()


if __name__ == "__main__":
    # main execution
    terminal_thread = threading.Thread(target=terminal_interface)
    receive_thread = threading.Thread(target=receive_messages)

    terminal_thread.start()
    receive_thread.start()
