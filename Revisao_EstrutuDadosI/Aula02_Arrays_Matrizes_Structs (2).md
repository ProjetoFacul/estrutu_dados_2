# Compilação de Algoritmos em C - Vetores, Matrizes e Registros (Structs)

---

# Exercício 1: Média e Soma de Elementos em um Vetor

```c
#include <stdio.h>
#include <string.h>

int main() {
    int m = 0;
    int s = 0;
    int vet[10]; 
    
    for (int i = 0; i < 10; i++) { 
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
```

---

# Exercício 2: Maior e Menor Valor em um Vetor com Posições

```c
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
```

---

# Exercício 3: Filtrar e Somar Números Pares em um Vetor

```c
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
```

---

# Exercício 4: Exibição de Vetor na Ordem Normal e Invertida

```c
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
```

---

# Exercício 5: Maior Valor e Soma em uma Matriz 3x3

```c
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
            
            if (i == 0 && j == 0) {
                maior = mat[i][j];
            } else if (mat[i][j] > maior) {
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
```

---

# Exercício 6: Diagonal Principal de uma Matriz 4x4

```c
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
```

---

# Exercício 7: Cálculo de Médias de Alunos com Matriz

```c
#include <stdio.h>

int main() {
    int s, m = 0;
    int mat[4][3];

    for (int i = 0; i < 4; i++) {
        for (int j = 0; j < 3; j++) {
            printf("Qual a %d nota do %d aluno: ", j + 1, i + 1);
            scanf("%d", &mat[i][j]);
        }
    }

    for (int i = 0; i < 4; i++) {
        s = 0;  

        for (int j = 0; j < 3; j++) {
            s += mat[i][j];
        }

        m = s / 3;

        printf("A media do aluno %d e: %d\n", i + 1, m);
    }

    return 0;
}
```

---

# Exercício 8: Cadastro de Produtos e Controle de Estoque (Structs)

```c
#include <stdio.h>

struct Produto {
    char nome[50];
    int codigo;
    float preco;
    int quantidade;
};

int main() {
    struct Produto produtos[5];

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
```

---

# Exercício 9: Sistema de Gestão de Notas de Alunos

```c
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

    for (int i = 0; i < 5; i++) {
        float media = (alunos[i].nota1 +
                        alunos[i].nota2 +
                        alunos[i].nota3) / 3;

        printf("\nAluno: %s", alunos[i].nome);
        printf("\nMedia: %.2f", media);

        if (media >= 7.0) {
            printf("\nStatus: Aprovado");
            aprovados++;
        } else {
            printf("\nStatus: Reprovado");
            reprovados++;
        }

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
```

---

# Exercício 10: Sistema Completo de Gerenciamento de Funcionários (Menu Interativo)

```c
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
        else if (opcao == 4) {
            float soma = 0;
            float media;

            for (int i = 0; i < 10; i++) {
                soma += funcionarios[i].salario;
            }

            media = soma / 10;

            printf("\nMedia salarial: %.2f\n", media);
        }
        else if (opcao == 5) {
            float soma = 0;
            float media;

            for (int i = 0; i < 10; i++) {
                soma += funcionarios[i].salario;
            }

            media = soma / 10;

            printf("\n===== ACIMA DA MEDIA =====\n");
            printf("Media salarial: %.2f\n", media);

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
```
