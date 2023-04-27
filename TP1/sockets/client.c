#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <time.h>


int delta() {
    // Definir a seed baseada no tempo
    srand(time(NULL));
    sleep(1);
    // Gerar número entre 1 e 100
    int number = rand() % 100 + 1;
    return number;
}

int main(int argc, char **argv) {
    // Definimos as variáveis do socket, endereço do servidor e o buffer que será preenchido para 
    // enviar os números ao servidor.
    int client_socket;
    int connect_status;
    struct sockaddr_in server_addr;
    int port_number = 5555;
    int n_iter = atoi(argv[1]);
    char buffer[20];

    // Abrimos o socket
    client_socket = socket(AF_INET, SOCK_STREAM, 0);
    if (client_socket != -1) {
	    printf("Client socket has been created.\n");
    } else {
        printf("Socket cannot be created.\n");
        return 1;
    }
    
    // Definimos o endereço e a porta em que o socket irá se conectar
    memset(&server_addr, '\0', sizeof(server_addr));
	server_addr.sin_family = AF_INET;
	server_addr.sin_port = htons(port_number);
	server_addr.sin_addr.s_addr = htonl(INADDR_LOOPBACK);

    // Conectamos o cliente ao servidor
    connect_status = connect(client_socket, (struct sockaddr *) &server_addr, sizeof(server_addr));
    if (connect_status == 0) {
        printf("Client successful connected to the server.\n");
    } else {
        close(client_socket);
        printf("Error connecting the client to the server.\n");
        return 1;
    }

    int n = 1;
    for (int i = 0; n_iter > i; i++) {
        // convertemos o n em string para depois enviarmos ao servidor
        sprintf(buffer, "%d", n);
        send(client_socket, buffer, 20, 0);
        printf("Sending data: %s\n", buffer);

        recv(client_socket, buffer, 20, 0);

        int n_size = strlen(buffer);
        if (buffer[n_size - 1] == 'p') {
            printf("%d is a prime number!\n", n);
        }

        n += delta();
    }

    n = 0;
    sprintf(buffer, "%d", n);
    send(client_socket, buffer, 20, 0);
    printf("Sending data: %s\n", buffer);
    close(client_socket);

    return 0;

}