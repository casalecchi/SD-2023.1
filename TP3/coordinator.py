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
# locks
queue_lock = threading.Lock()
critical_lock = threading.Lock()
log_lock = threading.Lock()
release_lock = threading.Lock()


# terminal thread
def terminal_interface():
    global close_socket, messages_queue, access_stats

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
    global close_socket, queue_lock, log_lock, messages_queue

    # create socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(COORD_ADDR)
    sock.listen(socket.SOMAXCONN)

    while not close_socket:
        # waiting for a connection
        client, _ = sock.accept()
        data = client.recv(MESSAGE_SIZE)

        # acquire on queue and log lock
        queue_lock.acquire()
        log_lock.acquire()
        
        # if message is release, set flag
        # else, (message is request) then put on queue
        # in both ways, write on log
        release_flag = False
        write_to_log(data, log_file)
        
        data_type, _ = decode_message(data)
        if data_type == 3:
            release_flag = True
        else:
            messages_queue.append(data)
            
        queue_lock.release()
        log_lock.release()
        

        # create new thread to process new message
        process_thread = threading.Thread(target=process_request, args=(client,release_flag,data))
        process_thread.start()

    sock.close()


# thread to process messages
def process_request(client: socket, release_flag: bool, release_message: bytes):
    # Arguments passed: client socket, flag if message is a release and the message itself

    global log_lock, queue_lock, critical_lock, messages_queue, access_stats

    # release messages will be priority
    # release section will have a lock to prevent two releases be in execute
    # in unexpected order
    if release_flag:
        release_lock.acquire()
        _, pid = decode_message(release_message)
        # compute statistics
        access_stats[pid] = access_stats.get(pid, 0) + 1
        # free critical section
        critical_lock.release()
        release_lock.release()
        return

    # the message sent was a request
    critical_lock.acquire()

    # get the first message on queue
    queue_lock.acquire()
    next_message = messages_queue.popleft()
    queue_lock.release()

    # get pid of message
    _, pid = decode_message(next_message)

    # create the permission message
    grant_message = create_grant_message(pid, MESSAGE_SIZE)
    data = grant_message.encode()

    # write grant permission on log
    log_lock.acquire()
    write_to_log(data, log_file)
    log_lock.release()

    # finally, send the permission to client
    client.send(data)


if __name__ == "__main__":
    # main execution
    terminal_thread = threading.Thread(target=terminal_interface)
    receive_thread = threading.Thread(target=receive_messages)

    terminal_thread.start()
    receive_thread.start()
