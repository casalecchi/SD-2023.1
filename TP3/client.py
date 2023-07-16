import socket
from time import sleep
from datetime import datetime
import os
import sys
from messages import *


COORD_ADDR = ("localhost", 8000)
MESSAGE_SIZE = 10
PID = os.getpid()

def client_process(r, k): 
    for i in range(r):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(COORD_ADDR) 
        # Envie uma mensagem de solicitação ao coordenador
        request_message = create_request_message(PID, MESSAGE_SIZE)
        encoded_request = request_message.encode()
        sock.send(encoded_request)
        print(f"Requisição do {request_message} enviada")
        
        # Aguarde a resposta do coordenador
        print("Esperando liberação...")
        data = sock.recv(MESSAGE_SIZE)
        print(f"Liberação do coordenador: {data}")

        sock.close()

        decoded_msg = data.decode()
        msg_type, _, _ = decoded_msg.split("|")

        # Verifique se o acesso foi concedido (verificar a mensagem de resposta)
        if msg_type == '2':
            # Acesso concedido, execute as operações na região crítica
            with open("resultado.txt", "a") as file:
                current_time = datetime.now()
                file.write(f"{PID} - {current_time}\n")

            # Aguarde k segundos antes de fazer a próxima solicitação
            sleep(k)
        
        # Se conecta novamente, para mandar outra mensagem
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(COORD_ADDR)

        release_message = create_release_message(PID, MESSAGE_SIZE)
        encoded_release = release_message.encode()
        print(f"Saindo da RC... {release_message}")
        sock.send(encoded_release)

        # Encerre o socket
        sock.close()
        

    

if __name__ == "__main__":
    inputs = sys.argv
    r, k = map(lambda x: int(x), inputs[1:])
    client_process(r, k)
