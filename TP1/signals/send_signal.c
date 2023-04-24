#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <signal.h>

void send_signal(pid_t pid, char *signal) {
    // Aqui faremos a comparação da string passada como argumento com o
    // sinal que será enviado.
    int confirmation;
    if (strcmp(signal, "SIGINT") == 0) {
        confirmation = kill(pid, SIGINT);
    } else if (strcmp(signal, "SIGTERM") == 0) {
        confirmation = kill(pid, SIGTERM);
    } else if (strcmp(signal, "SIGABRT") == 0) {
        confirmation = kill(pid, SIGABRT);
    }
    
    // Como a função kill retorna 0 quando o sinal é enviado de maneira
    // bem sucedida, é feito uma confirmação para o usuário do que aconteceu.
    if (confirmation == 0) {
        printf("Signal %s sent to the process %d\n", signal, pid);
    } else {
        printf("Couldn't sent the signal %s to the process\n", signal);
        exit(1);
    }
}

int main(int argc, char **argv) {
    // Aqui pegamos os parâmetros passados na linha de comando
    // O PID do processo em que o sinal será mandado
    pid_t pid = atoi(argv[1]);
    // E também o sinal que queremos enviar
    char *signal = argv[2];

    // Chamando a função kill com o sinal 0, teremos uma verificação
    // do pid, retornando zero caso ele seja válido.
    int verify_pid = kill(pid, 0);
    if (verify_pid != 0) {
        printf("Invalid pid: %d\n", pid);
        return 1;
    }

    send_signal(pid, signal);

    printf("PID: %d\n", pid);
    printf("Signal type: %s\n", signal);

    return 0;
}