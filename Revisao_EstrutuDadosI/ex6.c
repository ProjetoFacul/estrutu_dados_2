#include <stdio.h>

int main() {
 int s = 0;
 int mat[4][4];

 
 for (int i = 0; i <= 3; i++) {
  for (int j = 0; j <= 3; j++) {
  
  printf("Qual o valor para a posição [%d][%d]", i, j);
  scanf("%d", &mat[i][j]);
  
  }
 }
 
  printf("Matriz completa: \n");
  for (int i = 0; i <= 3; i++) {
   for (int j = 0; j <= 3; j++) {
  
  printf(" [%d] ", mat[i][j]);
  
  }
  printf("\n");
 }
 
 printf("Diagonal principal: \n");
 for (int i = 0; i <= 3; i++) {
  int j = i;
  s += mat[i][j];
  printf("[%d]", mat[i][j]);
 }
 printf("\nTotal dos valores da diagonal principal: %d", s); 


 return 0;
}