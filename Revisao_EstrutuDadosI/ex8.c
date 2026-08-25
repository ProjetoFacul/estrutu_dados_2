#include <stdio.h>

struct Produto {
    char nome[50];
    int codigo;
    float preco;
    int quantidade;
};

int main() {

    struct Produto produtos[5];

    // Cadastro dos produtos
    for (int i = 0; i < 5; i++) {

        printf("\nProduto %d\n", i + 1);

        printf("Nome: ");
        scanf("%49s", produtos[i].nome);

        printf("Codigo: ");
        scanf("%d", &produtos[i].codigo);

        printf("Preco: ");
        scanf("%f", &produtos[i].preco);

        printf("Quantidade: ");
        scanf("%d", &produtos[i].quantidade);
    }

    // Mostrar os produtos e calcular valor em estoque
    float maior_valor = 0;
    int pos_maior = 0;

    printf("\n===== PRODUTOS CADASTRADOS =====\n");

    for (int i = 0; i < 5; i++) {

        float valor_total = produtos[i].preco * produtos[i].quantidade;

        printf("\nProduto: %s\n", produtos[i].nome);
        printf("Codigo: %d\n", produtos[i].codigo);
        printf("Preco: %.2f\n", produtos[i].preco);
        printf("Quantidade: %d\n", produtos[i].quantidade);
        printf("Valor total em estoque: %.2f\n", valor_total);

        if (valor_total > maior_valor) {
            maior_valor = valor_total;
            pos_maior = i;
        }
    }

    printf("\n===== MAIOR VALOR EM ESTOQUE =====\n");
    printf("Produto: %s\n", produtos[pos_maior].nome);
    printf("Valor em estoque: %.2f\n", maior_valor);

    return 0;
}