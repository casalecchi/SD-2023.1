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

### Guia de uso - Sockets
