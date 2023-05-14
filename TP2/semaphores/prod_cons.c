#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <pthread.h>
#include <stdbool.h>
#include <semaphore.h>
#include <time.h>


sem_t *mutex, *empty, *full;
int buffer[1];
int position = 0;
int items_consumed = 0;
int item_limit = 100000;

// Função geradora de número aleatório
int delta(int i) {
    // Definir a seed baseada no tempo
    srand(time(NULL) * i);

    // Gerar número entre 1 e 10000000 (10^7)
    int number = rand() % 10000000 + 1;
    return number;
}

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

void *produce(void *arg) {
    int i = 1;
    while (1) {
        // Gera o número
        int number = delta(i);
        sem_wait(empty);
        sem_wait(mutex);
        
        if (items_consumed >= item_limit) {
            sem_post(mutex);
            sem_post(empty);
            sem_post(full);
            break;
        }

        buffer[position] = number;
        position++;
        
        sem_post(mutex);
        sem_post(full);
        i++;
        // printf("Number %d produced.\n", number);
    }
    return NULL;
}

void *consume(void *arg) {
    while (1) {
        sem_wait(full);
        sem_wait(mutex);
        
        if (items_consumed >= item_limit) {
            // Os dois primeiros liberam o semáforo para outra thread produtora terminar
            sem_post(mutex);
            sem_post(full);

            // Libera para as threads consumidoras terminarem
            sem_post(empty);
            break;
        }

        int number = buffer[position - 1];
        position--;
        items_consumed++;
        sem_post(mutex);
        sem_post(empty);
        
        if (is_prime(number)) {
            printf("Prime number %d consumed!\n", number);
        } else {
            printf("num\n");
        }
        printf("Items: %d\n", items_consumed);
    }
    return NULL;
}

int main(int argc, char **argv) {
    int np = atoi(argv[1]);
    int nc = atoi(argv[2]);

    pthread_t threads_p[np];
    pthread_t threads_c[nc];

    // No MacOS o uso de sem_init não funciona - https://stackoverflow.com/questions/36755003/initialise-semaphores-using-sem-open
    sem_unlink("/mutex");
    sem_unlink("/empty");
    sem_unlink("/full");
    
    mutex = sem_open("/mutex", O_CREAT | O_EXCL, S_IRWXU, 1);
    empty = sem_open("/empty", O_CREAT | O_EXCL, S_IRWXU, 1);
    full = sem_open("/full", O_CREAT | O_EXCL, S_IRWXU, 0);

    clock_t start_threads, stop_threads;
    start_threads = clock();

    for (int i = 0; i < np; i++) {
        if (pthread_create(&threads_p[i], NULL, produce, NULL) != 0) {
            printf("Error creating producer thread %d\n", i);
        }
    }

    for (int i = 0; i < nc; i++) {
        if (pthread_create(&threads_c[i], NULL, consume, NULL) != 0) {
            printf("Error creating consumer thread %d\n", i);
        }
    }

    for (int i = 0; i < nc; i++) {
        if (pthread_join(threads_c[i], NULL) != 0) {
            printf("Cannot wait for consumer thread %d\n", i);
        }
        printf("%d %d\n", i, nc);
    }

    for (int i = 0; i < np; i++) {
        if (pthread_join(threads_p[i], NULL) != 0) {
            printf("Cannot wait for produce thread %d\n", i);
        }
    }

    stop_threads = clock();
    printf("Tempo: %.5f\n", ((double) (stop_threads - start_threads) / CLOCKS_PER_SEC));

    // No MacOS o uso de sem_destroy não funciona - https://stackoverflow.com/questions/1413785/sem-init-on-os-x
    sem_close(mutex);
    sem_close(empty);
    sem_close(full);
}