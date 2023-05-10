#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <unistd.h>
#include <math.h>


int delta() {
    // Definir a seed baseada no tempo
    srand(time(NULL));

    // Gerar número entre 1 e 100
    int number = rand() % 201 - 100;
    return number;
}


int main(int argc, char **argv) {
    double power;
    int N;

    printf("Choose the power of 10 for buffer size [7 | 8 | 9]: ");
    scanf("%lf", &power);
    N = pow(10.0, power);
    printf("Buffer size = %d\n", N);

    int buffer[N];
    
    time_t start_time = time(NULL);

    for (int i = 0; i < N; i++) {
        int n = delta();
        printf("iteração: %d\n", i);
        buffer[i] = n;
    }

    time_t end_time = time(NULL);
    printf("Tempo para preencher o vetor: %lds\n", end_time - start_time);

    start_time = time(NULL);
    int counter = 0;
    for (int i = 0; i < N; i++) {
        counter += buffer[i];
    }
    end_time = time(NULL);

    printf("Tempo para somar o vetor: %lds\n", end_time - start_time);
    printf("%d\n", counter);
}