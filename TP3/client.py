import socket
from time import sleep
from datetime import datetime
import os
import sys
from messages import *

def client_process(coordinator_address, coordinator_port, r, k, process_id):
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
                current_time = datetime.now()
                file.write(f"{process_id} - {current_time}\n")

            # Aguarde k segundos antes de fazer a próxima solicitação
            sleep(k)
        

        # Se conecta novamente, para mandar outra mensagem
        release_message = create_release_message(process_id, 10)
        sock.send(release_message.encode())
        print(f"Saindo da RC... {release_message}")
        

    # Encerre o socket
    sock.close()

if __name__ == "__main__":
    inputs = sys.argv
    r, k = map(lambda x: int(x), inputs[1:])
    client_process("localhost", 8000, 3, 0, os.getpid())
