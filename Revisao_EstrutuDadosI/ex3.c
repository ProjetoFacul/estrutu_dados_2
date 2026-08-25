
#include <stdio.h>

int main() {
 int vet[20];
 int c = 0;
 int s = 0;
 
 for (int i = 0; i < 20; i++) {
  printf("Qual valor para a %d posição?", i + 1); 
  scanf("%d", &vet[i]);

 }
 
 
 printf("Pares: ");

  for (int i = 0; i < 20; i++) {
   
   if (vet[i] % 2 == 0) {
    c += 1;
    s += vet[i];
    printf("[%d]", vet[i]);
 }
  
  }
 printf("\nQuantidade de núemeros pares: %d\n", c);
 printf("A soma dos números pares é de: %d", s);
 
 return 0;
}