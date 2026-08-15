#include <stdio.h>
#include <stdlib.h>

int main() {

    // =========================
    // EXERCÍCIO 1: Inteiro dinâmico
    // =========================

    // Declara um ponteiro para inteiro e aloca dinamicamente
    // espaço suficiente para armazenar um valor inteiro.
    int *num = (int*) malloc(sizeof(int));

    // Verifica se a alocação de memória foi realizada com sucesso.
    // Caso malloc retorne NULL, significa que não foi possível
    // reservar a memória solicitada.
    if (num == NULL) {
        printf("Erro ao alocar memória para inteiro.\n");
        return 1;
    }

    // Armazena o valor 42 no espaço de memória apontado por num.
    *num = 42;

    printf("=== EXERCICIO 1 ===\n");

    // Exibe o valor armazenado na memória.
    printf("Valor: %d\n", *num);

    // Exibe o endereço de memória onde o valor foi armazenado.
    printf("Endereco: %p\n\n", (void*)num);

    // Libera a memória que foi alocada anteriormente.
    free(num);


    // =========================
    // EXERCÍCIO 2: String dinâmica
    // =========================

    // Ponteiro que será utilizado para armazenar a string.
    char *str;

    // Variável que armazenará o tamanho desejado para a string.
    int tamanho;

    printf("=== EXERCICIO 2 ===\n");
    printf("Digite o tamanho da string: ");
    scanf("%d", &tamanho);

    // Remove o '\n' que fica no buffer de entrada após o scanf.
    getchar();

    // Aloca memória para armazenar a quantidade de caracteres
    // informada pelo usuário + 1 posição para o caractere '\0',
    // que indica o final de uma string em C.
    str = (char*) malloc((tamanho + 1) * sizeof(char));

    // Verifica se a alocação foi realizada com sucesso.
    if (str == NULL) {
        printf("Erro ao alocar memória para string.\n");
        return 1;
    }

    printf("Digite uma frase: ");

    // Lê a frase digitada pelo usuário.
    // O tamanho máximo é tamanho + 1, considerando o '\0'.
    fgets(str, tamanho + 1, stdin);

    // Exibe a string armazenada na memória dinâmica.
    printf("String digitada: %s\n\n", str);

    // Libera a memória utilizada pela string.
    free(str);


    // =========================
    // EXERCÍCIO 3: Vetor dinâmico de inteiros
    // =========================

    // Ponteiro que será utilizado para armazenar o vetor.
    int *vetor;

    // Variável que armazenará a quantidade de números.
    int n;

    printf("=== EXERCICIO 3 ===\n");
    printf("Quantos numeros deseja armazenar? ");
    scanf("%d", &n);

    // Aloca dinamicamente memória suficiente para armazenar
    // n valores inteiros.
    vetor = (int*) malloc(n * sizeof(int));

    // Verifica se a alocação foi realizada com sucesso.
    if (vetor == NULL) {
        printf("Erro ao alocar memória para vetor.\n");
        return 1;
    }

    // Percorre o vetor e solicita os números ao usuário.
    for (int i = 0; i < n; i++) {
        printf("Digite o numero %d: ", i + 1);
        scanf("%d", &vetor[i]);
    }

    printf("Valores armazenados:\n");

    // Percorre novamente o vetor para mostrar
    // todos os valores armazenados.
    for (int i = 0; i < n; i++) {
        printf("%d ", vetor[i]);
    }

    printf("\n");

    // Libera a memória utilizada pelo vetor.
    free(vetor);

    return 0;
}