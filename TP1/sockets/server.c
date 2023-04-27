#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <stdbool.h>


bool is_prime(int n) {
    for (int i = 2; i < n; i++) {
        if (n % i == 0) {
            return false;
        }
    }
    return true;
}


int main(int argc, char **agrv) {
    // Definimos as variáveis do socket, endereço do servidor e o buffer que será preenchido para 
    // enviar os números ao servidor.
    int sockfd;
    struct sockaddr_in server_addr;
    int port_number = 5555;

    int new_socket;
    struct sockaddr_in new_addr;

    socklen_t addr_size;
    char buffer[20];

    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd != -1) {
	    printf("Server socket has been created.\n");
    } else {
        printf("Socket cannot be created.\n");
        return 1;
    }
	
    memset(&server_addr, '\0', sizeof(server_addr));
	server_addr.sin_family = AF_INET;
	server_addr.sin_port = htons(port_number);
	server_addr.sin_addr.s_addr = htonl(INADDR_ANY);

	int bind_socket = bind(sockfd, (struct sockaddr*) &server_addr, sizeof(server_addr));
    if (bind_socket == 0) {
	    printf("Binding to port number %d\n", port_number);
    } else {
        printf("Unable to bind to port number %d. Closing the socket...\n", port_number);
        close(sockfd);
        return 1;
    }

	int listen_socket = listen(sockfd, 1);
    if (listen_socket == 0) {
	    printf("Waiting for the client...\n");
    }

	new_socket = accept(sockfd, (struct sockaddr*) &new_addr, &addr_size);
    if (new_socket != -1) {
        printf("Connection was established with the client.\n");
    } else {
        printf("Connection cannot be established. Closing the socket...\n");
        close(sockfd);
        return 1;
    }

    int n = 1;
	while (n != 0) {
        // Recebendo o número gerado
        recv(new_socket, buffer, 20, 0);
        
        // Convertendo em int
        n = atoi(buffer);
        printf("Received data: %s\n", buffer);

        char prime;
        if (is_prime(n)) {
            prime = 'p';
        } else {
            prime = 'd';
        }

        // Convertendo o int n em string e adicionando um caracter ao final para indicar se
        // ele é primo ou não.
        sprintf(buffer, "%d%c", n, prime);
        printf("Sending data: %s\n", buffer);

        send(new_socket, buffer, 20, 0);
    }
	
    close(new_socket);
	printf("[+]Closing the connection.\n");
    close(sockfd);

}