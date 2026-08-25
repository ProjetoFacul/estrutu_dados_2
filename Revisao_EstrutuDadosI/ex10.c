#include <stdio.h>

struct Funcionario {
    char nome[50];
    int idade;
    char cargo[50];
    float salario;
};

int main() {

    struct Funcionario funcionarios[10];

    int opcao;

    do {

        printf("\n=================================\n");
        printf("       SISTEMA DE FUNCIONARIOS\n");
        printf("=================================\n");
        printf("1 - Cadastrar funcionarios\n");
        printf("2 - Listar funcionarios\n");
        printf("3 - Maior salario\n");
        printf("4 - Media salarial\n");
        printf("5 - Salarios acima da media\n");
        printf("0 - Sair\n");
        printf("Escolha uma opcao: ");
        scanf("%d", &opcao);

        // 1 - CADASTRAR
        if (opcao == 1) {

            for (int i = 0; i < 10; i++) {

                printf("\nFuncionario %d\n", i + 1);

                printf("Nome: ");
                scanf("%49s", funcionarios[i].nome);

                printf("Idade: ");
                scanf("%d", &funcionarios[i].idade);

                printf("Cargo: ");
                scanf("%49s", funcionarios[i].cargo);

                printf("Salario: ");
                scanf("%f", &funcionarios[i].salario);
            }
        }

        // 2 - LISTAR
        else if (opcao == 2) {

            printf("\n===== FUNCIONARIOS =====\n");

            for (int i = 0; i < 10; i++) {

                printf("\nFuncionario %d\n", i + 1);
                printf("Nome: %s\n", funcionarios[i].nome);
                printf("Idade: %d\n", funcionarios[i].idade);
                printf("Cargo: %s\n", funcionarios[i].cargo);
                printf("Salario: %.2f\n", funcionarios[i].salario);
            }
        }

        // 3 - MAIOR SALARIO
        else if (opcao == 3) {

            float maior = funcionarios[0].salario;
            int pos_maior = 0;

            for (int i = 1; i < 10; i++) {

                if (funcionarios[i].salario > maior) {
                    maior = funcionarios[i].salario;
                    pos_maior = i;
                }
            }

            printf("\n===== MAIOR SALARIO =====\n");
            printf("Funcionario: %s\n", funcionarios[pos_maior].nome);
            printf("Salario: %.2f\n", maior);
        }

        // 4 - MEDIA SALARIAL
        else if (opcao == 4) {

            float soma = 0;
            float media;

            for (int i = 0; i < 10; i++) {
                soma += funcionarios[i].salario;
            }

            media = soma / 10;

            printf("\nMedia salarial: %.2f\n", media);
        }

        // 5 - SALARIOS ACIMA DA MEDIA
        else if (opcao == 5) {

            float soma = 0;
            float media;

            // Primeiro calculamos a soma
            for (int i = 0; i < 10; i++) {
                soma += funcionarios[i].salario;
            }

            // Depois calculamos a media
            media = soma / 10;

            printf("\n===== ACIMA DA MEDIA =====\n");
            printf("Media salarial: %.2f\n", media);

            // Agora procuramos quem está acima dela
            for (int i = 0; i < 10; i++) {

                if (funcionarios[i].salario > media) {

                    printf("\nNome: %s\n", funcionarios[i].nome);
                    printf("Salario: %.2f\n", funcionarios[i].salario);
                }
            }
        }

        else if (opcao != 0) {
            printf("\nOpcao invalida!\n");
        }

    } while (opcao != 0);

    printf("\nPrograma encerrado.\n");

    return 0;
}