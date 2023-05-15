#include <stdlib.h>
#include <stdio.h>
#include <sys/time.h>
#include <unistd.h>
#include <math.h>
#include <stdatomic.h>
#include <pthread.h>


// Definição de variáveis globais -> buffer, tamanho do buffer, número de threads,
// contador compartilhado e a flag atômica que será usada como lock
const int N = 1000000000;
signed char buffer[N];
int K;
int counter = 0;
atomic_flag lock = ATOMIC_FLAG_INIT;


// Função geradora de número aleatório
signed char delta(int i) {
    // Definir a seed baseada no tempo
    srand(time(NULL) * i);

    // Gerar número entre -100 e 100
    signed char number = rand() % 201 - 100;
    return number;
}

// Função para preencher o buffer
void fill_buffer() {
    for (int i = 0; i < N; i++) {
        signed char n = delta(i);
        buffer[i] = n;
    }
}

// Função para entrar na região crítica
void acquire(atomic_flag *flag) {
    while(atomic_flag_test_and_set(flag));
}

// Função para sair da região crítica
void release(atomic_flag *flag) {
    atomic_flag_clear(flag);
}

// Função que as threads irão rodar
void *thread_sum(void *arg) {
    // É passado como argumento o número da thread para saber qual parcela da soma ela será responsável
    int thread_num = *(int*) arg;
    
    // Calculamos o tamanho da sua parcela
    int fraction = N / K;

    // As parcelas podem ficar desiguais em algumas combinações de N e K
    // Caso seja a última thread criada, o resto da divisão será adicionado 
    // a quantidade de números que devem ser somados
    int remainder = 0;
    if (thread_num == K - 1) {
        remainder += N % K;
    }

    int size = fraction + remainder;
    // Teremos um contador local da thread para somar os números de sua parcela
    int th_counter = 0;
    for (int i = 0; i < size; i++) {
        th_counter += buffer[i + thread_num * fraction];
    }

    // Região crítica da função: onde acessamos o contador principal e adicionamos
    // o valor da parcela da thread
    acquire(&lock);
    counter += th_counter;
    release(&lock);

    free(arg);
    return NULL;
}


int main(int argc, char **argv) {
    K = atoi(argv[1]);

    // Vetor de threads
    pthread_t threads[K];
    // Variáveis para calcular o tempo da soma utilizando threads
    struct timeval begin, end;

    fill_buffer();

    gettimeofday(&begin, 0);

    // Criação das threads
    for (int i = 0; i < K; i++) {
        int *thread_num = malloc(sizeof(int));
        *thread_num = i;
        if (pthread_create(&threads[i], NULL, *thread_sum, thread_num) != 0) {
            printf("Error creating thread %d\n", i);
        }
    }

    // Espera até que todas as threads retornem de suas execuções
    for (int i = 0; i < K; i++) {
        if (pthread_join(threads[i], NULL) != 0) {
            printf("Cannot wait for thread %d\n", i);
        }
    }

    gettimeofday(&end, 0);
    long seconds = end.tv_sec - begin.tv_sec;
    long microseconds = end.tv_usec - begin.tv_usec;
    double elapsed = seconds + microseconds*1e-6;

    // Verificação na thread principal para checar se valor calculado no contador 
    // utilizando threads confere
    int main_counter = 0;
    for (int i = 0; i < N; i++) {
        main_counter += buffer[i];
    }

    if (main_counter != counter) {
        printf("Sum calculated in main thread is different than calculated using threads.\n");
        return 1;
    }

    printf("%.5f\n", elapsed);
}