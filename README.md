# Sistemas Distribuídos
Repositório para os trabalhos práticos da disciplina COS470 - Sistemas Distribuídos.

## Trabalho Prático 1 - TP1

* Sinais
* Pipes
* Sockets

### Guia de uso - Sinais

Neste caso temos dois programas que serão rodados, o `receive_signal` e o `send_signal`. A primeira coisa que deve ser feita é compilar ambos utilizando o seguinte comando no terminal (é necessário estar no diretório signals):

```shell
gcc receive_signal.c -o receive
gcc send_signal.c -o send
```

Feita a compilação dos programas, primeiro devemos rodar o programa que irá receber o sinal indicando como parâmetro o tipo de espera que será realizada: 

```shell
./receive busy
```
ou

```shell
./receive blocking
```

Depois disso devemos rodar o programa que irá enviar sinais para esse primeiro, passando como argumentos, respectivamente, o PID do processo que foi printado na tela com o programa receive e o tipo de sinal que será mandado. Na nossa implementação escolhemos tratar 3 sinais, sendo eles:

* SIGINT
* SIGTERM
* SIGABRT

Quando um desses sinais é passado, ele é enviado ao processo e o processo printa confirmando o tipo de sinal que recebeu. O sinal que finaliza o processo é o SIGTERM.

A forma de utilizar o programa é da seguinte maneira:

```shell
./send PID TIPO_SINAL
```

### Guia de uso - Pipes

Passando agora para o programa em que os pipes são utilizados, é necessário compilar o código, da mesma maneira em que foi feita no caso dos sinais.

```shell
gcc prod_cons.c -o prod_cons
```

Nesse programa é apenas necessário passar um argumento, que é o número de iterações que serão realizadas. Portanto o uso para 100 iterações fica da seguinte maneira:

```shell
./prod_cons 100
```

### Guia de uso - Sockets

Finalizando, para utilizar os programas do socket é necessário compilar os códigos, da mesma maneira em que foi feita nos casos acima.

```shell
gcc server.c -o server
gcc client.c -o client
```

Primeiro é necessário executar o programa `server`, sem argumentos.

```shell
./server
```

Depois é a vez de executar o `client` passando o número de iterações que o programa irá executar.

```shell
./client 100
```

## Trabalho Prático 2 - TP2

* Somador com spinlocks
* Produtor Consumidor com semáforos

### Guia de uso - Somador

Seguindo os padrões anteriores no TP1, devemos compilar o código dessa maneira: 

```shell
gcc counter.c -o counter
```

O tamanho do vetor N está fixado em $10^9$, mas é possível mudá-lo no próprio código (lembra-se de fazer isso antes de compilá-lo). Já o número de threads que serão utilizadas para realizar a soma, o parâmetro $K$ é fornecido como argumento na linha de comando. Um exemplo do uso do programa com $K = 64$ threads é mostrado abaixo.

```shell
./counter 64
```

### Guia de uso - Produtor Consumidor

Primeiro é feita a compilação:

```shell
gcc prod_cons.c -o prod_cons
```

O tamanho do vetor N aqui é feito da mesma maneira que no programa somador. Este valor está fixado em 1000. Em seguida, teremos que passar dois parâmetros via linha de comando. Serão dois inteiros que indicam as quantidades de threads produtoras e consumidoras, respectivamente. É mostrado o caso onde rodamos o programa para 1 thread produtora e 8 threads consumidoras. 

```shell
./prod_cons 1 8
```
