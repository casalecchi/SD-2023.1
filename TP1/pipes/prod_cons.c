#include <stdio.h>
#include <stdbool.h>
#include <unistd.h>
#include <stdlib.h>
#include <time.h>


bool is_prime(int n) {
    for (int i = 2; i < n; i++) {
        if (n % i == 0) {
            return false;
        }
    }
    return true;
}

int delta() {
    // Definir a seed baseada no tempo
    srand(time(NULL));
    sleep(1);

    // Gerar número entre 1 e 100
    int number = rand() % 100 + 1;
    return number;
}

int main(int argc, char **argv) {
    // Criamos os descritores de arquivo
    int fd[2];

    // Criamos o pipe
    if (pipe(fd) == -1) {
        printf("Error has occur opening the pipe\n");
        return 1;
    }

    // Obtemos os números de iterações passadas como argumento
    int n_iter = atoi(argv[1]);
    
    // O comando fork() retorna 0 no processo filho e o pid do filho no processo pai
    pid_t id = fork();

    if (id < 0) {
        printf("Error has occur creating the fork\n");
        return 1;
    } else if (id == 0) {
        // Filho será o leitor/consumidor
        
        // Fechamos a ponta de escrita
        close(fd[1]);

        // Número X que será lido pelo pipe
        int x = 1;
        while (x != 0) {
            // Como ele é enviado como string, o recebemos como string e depois convertemos para int
            char str_number[20];
            read(fd[0], &str_number, 20);
            x = atoi(str_number);

            if (is_prime(x)) {
                printf("Consumer read %d and it's a prime number!\n", x);
            } 
        }

        // Após ler o número 0, a ponta de leitura é fechada
        close(fd[0]);
    } else {
        // Pai será o escritor/produtor

        // Fechamos a ponta de leitura
        close(fd[0]);

        // Definimos o n0 e o array para enviar o número como string
        int n = 1;
        char str_number[20];

        for (int iter = 0; iter < n_iter; iter++) {
            n += delta();
            
            // Conversão de int para string
            sprintf(str_number, "%d", n);
            
            write(fd[1], &str_number, 20);
        }

        // Após as iterações, é enviado o número 0 para indicar que as escritas acabaram
        n = 0;
        sprintf(str_number, "%d", n);
        write(fd[1], &str_number, 20);

        // Fechamos a ponta de escrita
        close(fd[1]);
    }

    return 0;
}