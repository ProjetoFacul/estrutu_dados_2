#include <stdio.h>
#include <string.h>

int main() {
    int m = 0;
    int s = 0;
    int vet[10]; // vet [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    for (int i = 0; i < 10; i++) { //[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        printf("Digite o valor %d valor: ", i + 1);
        scanf("%d", &vet[i]);
        s += vet[i];
    }
    m = s / 10;
    printf("Valor da soma %d\n", s);
    printf("Valor da media: %d\n", m);
    printf("Valor do vetor [vet] = ");
    for (int i = 0; i < 10; i++) {
        printf("[%d]", vet[i]);
        
    }
    
    return 0;
}
