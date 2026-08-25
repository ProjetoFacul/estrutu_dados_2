#include <stdio.h>

int main() {
 int s = 0;
 int mat[3][3];
 int maior = 0;
 
 for (int i = 0; i <= 2; i++) {
  for (int j = 0; j <= 2; j++) {
  
  printf("Qual o valor para a posição [%d][%d]", i, j);
  scanf("%d", &mat[i][j]);
  
  }
 }
 
  printf("Matriz: \n");
  for (int i = 0; i <= 2; i++) {
   for (int j = 0; j <= 2; j++) {
   s += mat[i][j];
   maior = mat[i][j];
   
   if (mat[i][j] > maior) {
    maior = mat[i][j];
   }
   
   printf("[%d] ", mat[i][j]);

  
  }
  printf("\n");
 }
 printf("Soma dos valores da matriz: %d\n", s);
 printf("O maior valor da matriz: %d", maior);
 return 0;
}