#include <stdio.h>

int main() {
    int maior_valor = 0;
    int menor_valor = 0;
    int pos_maior = 0;
    int pos_menor = 0;
    int vet[10];

    for (int i = 0; i < 10; i++) {
        printf("Digite o %d valor: ", i + 1);
        scanf("%d", &vet[i]);

        if (i == 0) {
            maior_valor = vet[i];
            menor_valor = vet[i];
            pos_maior = i;
            pos_menor = i;
        }

        if (vet[i] > maior_valor) {
            maior_valor = vet[i];
            pos_maior = i;
        }

        if (vet[i] < menor_valor) {
            menor_valor = vet[i];
            pos_menor = i;
        }
    }

    printf("O maior valor e %d, na posicao %d\n", maior_valor, pos_maior);
    printf("O menor valor e %d, na posicao %d\n", menor_valor, pos_menor);

    return 0;
}