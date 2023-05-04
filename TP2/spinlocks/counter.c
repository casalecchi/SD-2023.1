#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <unistd.h>
#include <math.h>


int buffer[10000000];

int delta() {
    // Definir a seed baseada no tempo
    srand(time(NULL));

    // Gerar número entre 1 e 100
    int number = rand() % 201 - 100;
    return number;
}


int main(int argc, char **argv) {
    for (int i = 0; i < 10000000; i++) {
        int n = delta();
        printf("N gerado: %d\n", n);
        printf("iteração: %d\n", i);
        buffer[i] = n;
    }

    int counter = 0;
    for (int i = 0; i < 10000000; i++) {
        counter += buffer[i];
    }

    printf("%d\n", counter);
}