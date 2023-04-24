#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <signal.h>
#include <string.h>


// Signal handlers dos sinais escolhidos
void sigint_handler(int num) {
    printf("SIGINT received by the process %d\n", getpid());
}

void sigterm_handler(int num) {
    // No SIGTERM ele irá terminar o processo
    printf("SIGTERM received by the process %d\n", getpid());
    exit(0);
}

void sigabrt_handler(int num) {
    printf("SIGABRT received by the process %d\n", getpid());
}

// Implementação das esperas
void busy_wait() {
    printf("Busy wait selected. Process ID: %d\n", getpid());
    while(1) {};
}

void blocking_wait() { 
    printf("Blocking wait selected. Process ID: %d\n", getpid());
    while(1) {
        // Função pause, seguindo a documentação, suspende a execução do programa até que um sinal chegue
        pause();
    }
}


int main(int argc, char **argv) {
    // É definido os tipos de sinais que o processo irá esperar para que os handlers sejam executados
    signal(SIGINT, sigint_handler);
    signal(SIGTERM, sigterm_handler);
    signal(SIGABRT, sigabrt_handler);

    // Lógica para escolher o tipo de espera
    char *wait_type = argv[1];
    if (strcmp(wait_type, "busy") == 0) {
        busy_wait();
    } else if (strcmp(wait_type, "blocking") == 0) {
        blocking_wait();
    } else {
        printf("Invalid argument: %s. Please select between [ busy | blocking ]\n", wait_type);
        exit(0);
    }
}