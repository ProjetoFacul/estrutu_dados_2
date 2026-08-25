#include <stdio.h>

int main() {
    int s, m = 0;
    int mat[4][3];

    // Preenchendo a matriz
    for (int i = 0; i < 4; i++) {
        for (int j = 0; j < 3; j++) {
            printf("Qual a %d nota do %d aluno: ", j + 1, i + 1);
            scanf("%d", &mat[i][j]);
        }
    }

    // Calculando a média de cada aluno
    for (int i = 0; i < 4; i++) {
        s = 0;  // começa uma nova soma para cada aluno

        for (int j = 0; j < 3; j++) {
            s += mat[i][j];
        }

        m = s / 3;

        printf("A media do aluno %d e: %d\n", i + 1, m);
    }

    return 0;
}