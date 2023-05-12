#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <unistd.h>
#include <math.h>
#include <pthread.h>


int buffer[100000];
int N = 100000;
int K = 2;

int delta(int i) {
    // Definir a seed baseada no tempo
    srand(time(NULL) * i);

    // Gerar número entre 1 e 100
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

void *thread_sum(void *arg) {
    int thread_num = *(int*) arg;
    int size = N / K;
    int th_counter = 0;
    for (int i = 0; i < size; i++) {
        th_counter += buffer[i + thread_num * size];
    }
    return NULL;
}


int main(int argc, char **argv) {
    pthread_t threads[K];

    fill_buffer();

    for (int i = 0; i < K; i++) {
        if (pthread_create(&threads[i], NULL, *fill_buffer, NULL) != 0) {
            printf("Error creating thread %d\n", i);
        }
    }

    for (int i = 0; i < K; i++) {
        if (pthread_join(threads[i], NULL) != 0) {
            printf("Cannot wait for thread %d\n", i);
        }
    }
}