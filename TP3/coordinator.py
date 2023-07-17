import os
import socket
import threading
from utils import *
from queue import Queue
from datetime import datetime

MESSAGE_SIZE = 10
CLOSE_SOCKET = False
COORD_ADDR = ("localhost", 8000)

queue_sem = threading.Semaphore(1)
critical_sem = threading.Semaphore(1)
log_sem = threading.Semaphore(1)

request_queue = Queue()
access_stats = {}
counter = 0

logname = 'log.txt'

def terminal_interface():
    while True:
        command = input("Digite o comando: ")

        if command == "fila":
            print(request_queue.queue)
        elif command == "estatisticas":
            print(access_stats)
        elif command == "encerrar":
            # Encerra a execução do coordenador
            CLOSE_SOCKET = True
            os._exit(0)
        else:
            print("Comando inválido")



# Receber pedidos, colocar na fila e criar threads de processamento
def receive_requests():
    global CLOSE_SOCKET

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(COORD_ADDR)
    sock.listen(socket.SOMAXCONN)

    while not CLOSE_SOCKET:
        # Waiting for a message
        client, addr = sock.accept()
        data = client.recv(MESSAGE_SIZE)
        
        log_message = create_log_message(data)
        log_sem.acquire()
        with open(logname, "a") as file:
            file.write(log_message)
        log_sem.release()

        if data == b"":
            print(" ISSO RODA ??????")
            client.close()
            break 
        
        queue_sem.acquire()
        request_queue.put(data)
        queue_sem.release()

        process_thread = threading.Thread(target=process_request, args=(client,))
        process_thread.start()

    sock.close()


def process_request(client):
    global counter

    queue_sem.acquire()
    request = request_queue.get()
    queue_sem.release()

    message_type, pid = decode_message(request)

    # Take actions based on the received request (grant access, update statistics, etc.)
    if message_type == 1:
        critical_sem.acquire()
        grant_message = create_grant_message(pid, MESSAGE_SIZE)
        data = grant_message.encode()
        client.send(data)

        log_message = create_log_message(data)
        log_sem.acquire()
        with open(logname, "a") as file:
            file.write(log_message)
        log_sem.release()

    if message_type == 3:
        counter += 1
        access_stats[pid] = access_stats.get(pid, 0) + 1
        critical_sem.release()




if __name__ == "__main__":
    terminal_thread = threading.Thread(target=terminal_interface)
    receive_thread = threading.Thread(target=receive_requests)

    terminal_thread.start()
    receive_thread.start()
