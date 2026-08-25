#include <stdio.h>

int main() {

int vet[10];


 for (int i = 0; i < 10; i++) {
  printf("Qual o %d valor: ", i + 1);
  scanf("%d", &vet[i]);
 
 }
 
 printf("Vetor normal: ");
 for (int i = 0; i < 10; i++) {
  printf("[%d] ", vet[i]);
 
 }
 
 printf("\nVetor invertido: ");
 for (int i = 9; i >= 0; i--) {
  printf("[%d] ", vet[i]);
 }
 
 return 0;
}