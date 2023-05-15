#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <pthread.h>
#include <stdbool.h>
#include <semaphore.h>
#include <sys/time.h>


// Declaração de variáveis globais
// Semáforos usados, vetor, posição, itens consumidos e limite de itens
sem_t *mutex, *empty, *full;
const int N = 1000;
int buffer[N];
int position = 0;
int items_consumed = 0;
int item_limit = 100000;


// Declaração das funções acessórias, presentes no final do código
int delta(int i);
bool is_prime(int n);


// Função executada pelas threads produtoras
void *produce(void *arg) {
    // Variável i é usada apenas para ajudar na aleatoriedade
    int i = 1;

    while (1) {
        // Número é produzido
        int number = delta(i);

        // Semáforos são decrementados
        sem_wait(empty);
        sem_wait(mutex);
        
        // Dentro da região crítica é checado se o número de itens consumidos já chegou no limite estabelecido
        // para realizar um encerramento das threads
        if (items_consumed >= item_limit) {
            // O post no empty e mutex permite que outras threads produtoras sejam executadas e também encerrem
            sem_post(empty);
            sem_post(mutex);

            // O post no full permite que as threads consumidoras sejam executadas e encerradas
            sem_post(full);
            break;
        }

        // Vetor é preenchido no final e esse final é atualizado
        buffer[position] = number;
        position++;
        
        // Semáforos são incrementados
        sem_post(mutex);
        sem_post(full);
        i++;
    }

    return NULL;
}

// Função executada pelas threads consumidoras
void *consume(void *arg) {
    while (1) {
        // Semáforos são decrementados
        sem_wait(full);
        sem_wait(mutex);
        
        // O mesmo raciocínio para o encerramento de threads que foi explicado na função `produce` 
        // é realizado aqui
        if (items_consumed >= item_limit) {
            sem_post(mutex);
            sem_post(full);
            sem_post(empty);
            break;
        }

        // Número produzido é lido do vetor, final do vetor é decrementado 
        // e o número de itens consumidos é incrementado 
        int number = buffer[position - 1];
        position--;
        items_consumed++;

        // Semáforos são incrementados
        sem_post(mutex);
        sem_post(empty);
        
        // Número lido é processado (consumido)
        if (is_prime(number)) {
            // printf("Prime number %d consumed!\n", number);
        }
    }

    return NULL;
}

int main(int argc, char **argv) {
    // Parâmetros do programa como argumentos na linha de comando
    int np = atoi(argv[1]);  // threads produtoras
    int nc = atoi(argv[2]);  // threads consumidoras

    // Vetores de threads declarados
    pthread_t threads_p[np];
    pthread_t threads_c[nc];

    // No MacOS é possível utilizar apenas semáforos nomeados, portanto "limpamos" um 
    // semáforo antes de iniciá-lo para que seu uso seja correto
    // https://man7.org/linux/man-pages/man3/sem_unlink.3.html
    // https://stackoverflow.com/questions/26797126/why-sem-wait-doesnt-wait-semaphore-on-mac-osx
    sem_unlink("/mutex");
    sem_unlink("/empty");
    sem_unlink("/full");
    
    // No MacOS o uso de sem_init não funciona - https://stackoverflow.com/questions/36755003/initialise-semaphores-using-sem-open
    // https://man7.org/linux/man-pages/man3/sem_open.3.html
    // Inicializamos e abrimos o semáforo nomeado - parâmetros: nome, oflag, permissões e valor inicial 
    mutex = sem_open("/mutex", O_CREAT | O_EXCL, S_IRWXU, 1);
    empty = sem_open("/empty", O_CREAT | O_EXCL, S_IRWXU, N);
    full = sem_open("/full", O_CREAT | O_EXCL, S_IRWXU, 0);

    // Cálculo do tempo
    struct timeval begin, end;
    gettimeofday(&begin, 0);

    for (int i = 0; i < np; i++) {
        // Criação de threads produtoras
        if (pthread_create(&threads_p[i], NULL, produce, NULL) != 0) {
            printf("Error creating producer thread %d\n", i);
        }
    }

    for (int i = 0; i < nc; i++) {
        // Criação de threads consumidoras
        if (pthread_create(&threads_c[i], NULL, consume, NULL) != 0) {
            printf("Error creating consumer thread %d\n", i);
        }
    }

    for (int i = 0; i < nc; i++) {
        // Espera pela finalização de threads consumidoras
        if (pthread_join(threads_c[i], NULL) != 0) {
            printf("Cannot wait for consumer thread %d\n", i);
        }
    }

    for (int i = 0; i < np; i++) {
        // Espera pela finalização de threads produtoras
        if (pthread_join(threads_p[i], NULL) != 0) {
            printf("Cannot wait for produce thread %d\n", i);
        }
    }

    // Cálculo do tempo
    gettimeofday(&end, 0);
    long seconds = end.tv_sec - begin.tv_sec;
    long microseconds = end.tv_usec - begin.tv_usec;
    double elapsed = seconds + microseconds*1e-6;

    printf("Time taken: %.5fs\n", elapsed);

    // No MacOS o uso de sem_destroy não funciona - https://stackoverflow.com/questions/1413785/sem-init-on-os-x
    // Fechamos os semáforos usados
    sem_close(mutex);
    sem_close(empty);
    sem_close(full);

    return 0;
}

// Função geradora de números aleatórios
int delta(int i) {
    // Definir a seed baseada no tempo
    srand(time(NULL) * i);
    // Gerar número entre 1 e 10000000 (10^7)
    int number = rand() % 10000000 + 1;
    return number;
}

// Função que retorna se número é primo ou não
bool is_prime(int n) {
    if (n < 2) {
        return false;
    }
    for (int i = 2; i < n; i++) {
        if (n % i == 0) {
            return false;
        }
    }
    return true;
}