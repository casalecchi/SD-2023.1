import socket
import time
import os
from messages import *

def client_process(coordinator_address, coordinator_port, k, r, process_id):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  

    # conectar ao coordenador
    sock.connect((coordinator_address, coordinator_port))
    

    for i in range(r):
        # Envie uma mensagem de solicitação ao coordenador
        request_message = create_request_message(process_id, 10)
        sock.send(request_message.encode())
        print(f"Requisição do {request_message}")
        

        # Aguarde a resposta do coordenador
        response = sock.recv(10)
        print(f"Liberação do coordenador: {response}")

        message_type, _, _ = response.decode().split("|")

        # Verifique se o acesso foi concedido (verificar a mensagem de resposta)
        if message_type == '2':
            # Acesso concedido, execute as operações na região crítica
            with open("resultado.txt", "a") as file:
                current_time = time.time()
                file.write(f"{process_id} - {current_time}\n")

        # Aguarde k segundos antes de fazer a próxima solicitação
        time.sleep(k)

        # Se conecta novamente, para mandar outra mensagem
        release_message = create_release_message(process_id, 10)
        sock.send(release_message.encode())
        print(f"Saindo da RC... {release_message}")
        

    # Encerre o socket
    sock.close()

client_process("localhost", 8001, 2, 5, os.getpid())
