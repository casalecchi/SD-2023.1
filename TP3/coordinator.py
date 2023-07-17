import os
import socket
import threading
from messages import *
from queue import Queue
from datetime import datetime

MESSAGE_SIZE = 10
CLOSE_SOCKET = False
COORD_ADDR = ("localhost", 8000)

queue_sem = threading.Semaphore(1)
critic_sem = threading.Semaphore(1)

request_queue = Queue()
access_stats = {}
counter = 0

filename = 'coordinator_log.txt'

with open(filename, 'w') as file:
    pass

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
        print("Esperando pedido...")    
        client, addr = sock.accept()
        data = client.recv(MESSAGE_SIZE)
        decoded = data.decode()
        print("Pedido aceito")

        if decoded == "":
            break 
        
        queue_sem.acquire()
        request_queue.put(decoded)
        queue_sem.release()

        process_thread = threading.Thread(target=process_request, args=(client,))
        process_thread.start()

    sock.close()


def process_request(client):
    global counter
    queue_sem.acquire()
    print(request_queue.queue)
    request = request_queue.get()
    queue_sem.release()

    # Extract information from the request (message type, process ID)
    message_type, process_id, _ = request.split("|")

    # Take actions based on the received request (grant access, update statistics, etc.)
    if message_type == '1':
        critic_sem.acquire()
        with open("coordinator_log.txt", "a") as file:
            current_time = str(datetime.now())
            file.write(f"Instante de chegada da mensagem: {current_time[11:19]} ; Tipo da mensagem:{message_type} \
                         Processo de Origem {process_id} ; Processo Destino {os.getpid()} - \n")
        grant_message = create_grant_message(process_id, MESSAGE_SIZE)
        encoded_grant = grant_message.encode()
        client.send(encoded_grant)
        with open("coordinator_log.txt", "a") as file:
            current_time = str(datetime.now())
            file.write(f"Instante do envio da mensagem: {current_time[11:19]} ; Tipo da mensagem: 2 \
                         Processo de Origem {os.getpid()} ; Processo Destino {process_id} - \n")
        print(f"Mensagem de permissão enviada a {process_id}")

    if message_type == '3':
        counter += 1
        access_stats[process_id] = access_stats.get(process_id, 0) + 1
        with open("coordinator_log.txt", "a") as file:
            current_time = str(datetime.now())
            file.write(f"Instante de chegada da mensagem: {current_time[11:19]} ; Tipo da mensagem:{message_type} \
                         Processo de Origem {process_id} ; Processo Destino {os.getpid()} - \n")
        critic_sem.release()
        print(f"Mensagem de liberação de RC recebida {process_id}")




if __name__ == "__main__":
    terminal_thread = threading.Thread(target=terminal_interface)
    receive_thread = threading.Thread(target=receive_requests)

    terminal_thread.start()
    receive_thread.start()
