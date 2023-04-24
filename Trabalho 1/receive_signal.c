#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <signal.h>

void sigint_handler(int num) {
    printf("SIGINT received by the process %d\n", getpid());
}

void sigterm_handler(int num) {
    printf("SIGTERM received by the process %d\n", getpid());
    exit(0);
}

void sigabrt_handler(int num) {
    printf("SIGABRT received by the process %d\n", getpid());
}

int main(int argc, char **argv) {
    char *wait_type = argv[1];

    signal(SIGINT, sigint_handler);
    signal(SIGTERM, sigterm_handler);
    signal(SIGABRT, sigabrt_handler);

    while(1) {
        printf("My pid: %d\n", getpid());
        sleep(1);
    }
}