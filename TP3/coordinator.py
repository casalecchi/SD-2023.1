import threading
import socket
import os
from queue import Queue
from messages import *

MESSAGE_SIZE = 10
semaphore = threading.Semaphore(1)
request_queue = Queue()
access_stats = {}

# Crie um socket TCP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Vincule o socket a um endereço e porta
server_address = ("localhost", 8001)
sock.bind(server_address)
sock.listen(128)
print("Socket criado")

def terminal_interface():
    while True:
        command = input("Digite o comando: ")

        if command == "fila":
            print(request_queue.queue)
        elif command == "estatisticas":
            print(access_stats)
        elif command == "encerrar":
            # Encerra a execução do coordenador
            sock.close()
            os._exit(0)
        else:
            print("Comando inválido")


# Criar threads e recebr pedidos
def receive_requests():
    while True:
        print("Esperando cliente...")
        client, _ = sock.accept()
        print("Cliente aceito...")

        # Registrar o pedido no arquivo de log
        # log_message = create_log_message(data.decode(), address)
        # write_to_log(log_message)

        process_thread = threading.Thread(target=process_request, args=(client,))
        process_thread.start()


def process_request(client):
    while True:
        data = client.recv(10)
        print(f"Dado recebido: {data}")

        # Tratar data pra quando acabar as iterações !!!!!!!!

        # Processar o pedido recebido
        semaphore.acquire()
        request_queue.put(data.decode())
        semaphore.release()

        print("Chegou mensagem")
        semaphore.acquire()
        request = request_queue.get()
        
        # Extrair informações do pedido (identificador da mensagem, identificador do processo)
        message_type, process_id, _ = request.split("|")

        # Tomar decisões com base no pedido recebido (conceder acesso, atualizar estatísticas, etc.)
        if message_type == '1':
            grant_message = create_grant_message(process_id, 10)
            client.send(grant_message.encode())
            print(f"Mensagem de permissão enviada a {process_id}")

        msg = client.recv(10)
        print(msg)
        release, pid, _ = msg.decode().split("|")

        if release == '3':
            semaphore.release()
            print(f"Mensagem de liberação de RC recebida {pid}")


terminal_thread = threading.Thread(target=terminal_interface)
receive_thread = threading.Thread(target=receive_requests)

terminal_thread.start()
receive_thread.start()
