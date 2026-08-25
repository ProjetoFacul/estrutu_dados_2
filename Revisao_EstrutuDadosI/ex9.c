#include <stdio.h>

struct Aluno {
    char nome[50];
    int idade;
    float nota1;
    float nota2;
    float nota3;
};

int main() {

    struct Aluno alunos[5];

    int aprovados = 0;
    int reprovados = 0;

    float maior_media = 0;
    int pos_maior = 0;

    // Cadastro dos alunos
    for (int i = 0; i < 5; i++) {

        printf("\nAluno %d\n", i + 1);

        printf("Nome: ");
        scanf("%49s", alunos[i].nome);

        printf("Idade: ");
        scanf("%d", &alunos[i].idade);

        printf("Nota 1: ");
        scanf("%f", &alunos[i].nota1);

        printf("Nota 2: ");
        scanf("%f", &alunos[i].nota2);

        printf("Nota 3: ");
        scanf("%f", &alunos[i].nota3);
    }

    // Calculando as médias
    for (int i = 0; i < 5; i++) {

        float media = (alunos[i].nota1 +
                       alunos[i].nota2 +
                       alunos[i].nota3) / 3;

        printf("\nAluno: %s", alunos[i].nome);
        printf("\nMedia: %.2f", media);

        // Verifica aprovação
        if (media >= 7.0) {
            printf("\nStatus: Aprovado");
            aprovados++;
        } else {
            printf("\nStatus: Reprovado");
            reprovados++;
        }

        // Verifica maior média
        if (media > maior_media) {
            maior_media = media;
            pos_maior = i;
        }
    }

    printf("\n\n===== RESULTADO FINAL =====\n");

    printf("Aprovados: %d\n", aprovados);
    printf("Reprovados: %d\n", reprovados);

    printf("Aluno com maior media: %s\n", alunos[pos_maior].nome);
    printf("Maior media: %.2f\n", maior_media);

    return 0;
}