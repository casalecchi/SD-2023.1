#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <unistd.h>
#include <math.h>
#include <stdatomic.h>
#include <pthread.h>


int buffer[100000000];
int N = 100000000;
int K = 16;
int counter = 0;
atomic_flag lock = ATOMIC_FLAG_INIT;

int delta(int i) {
    // Definir a seed baseada no tempo
    srand(time(NULL) * i);

    // Gerar número entre -100 e 100
    int number = rand() % 201 - 100;
    return number;
}

void fill_buffer() {
    for (int i = 0; i < N; i++) {
        int n = delta(i);
        printf("iteração: %d\n", i);
        buffer[i] = n;
    }
}

void acquire(atomic_flag *flag) {
    while(atomic_flag_test_and_set(flag));
}

void release(atomic_flag *flag) {
    atomic_flag_clear(flag);
}

void *thread_sum(void *arg) {
    int thread_num = *(int*) arg;
    int size = N / K;
    int th_counter = 0;
    for (int i = 0; i < size; i++) {
        th_counter += buffer[i + thread_num * size];
    }

    acquire(&lock);
    counter += th_counter;
    release(&lock);

    free(arg);
    return NULL;
}


int main(int argc, char **argv) {
    pthread_t threads[K];

    fill_buffer();

    clock_t start_threads, stop_threads;

    start_threads = clock();

    for (int i = 0; i < K; i++) {
        int *thread_num = malloc(sizeof(int));
        *thread_num = i;
        if (pthread_create(&threads[i], NULL, *thread_sum, thread_num) != 0) {
            printf("Error creating thread %d\n", i);
        }
    }

    for (int i = 0; i < K; i++) {
        if (pthread_join(threads[i], NULL) != 0) {
            printf("Cannot wait for thread %d\n", i);
        }
    }

    stop_threads = clock();

    int main_counter = 0;
    for (int i = 0; i < N; i++) {
        main_counter += buffer[i];
    }

    if (main_counter != counter) {
        printf("Sum calculated in main thread is different than calculated using threads.\n");
        return 1;
    }

    printf("Main -> %d\n", main_counter);
    printf("Threads -> %d\n", counter);

    printf("Time calculate by threads: %.5f\n", ((double) (stop_threads - start_threads) / CLOCKS_PER_SEC));
}