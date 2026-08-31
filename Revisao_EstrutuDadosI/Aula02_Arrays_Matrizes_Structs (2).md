# Compilação de Algoritmos em C - Vetores, Matrizes e Registros (Structs)

---
```c
# 1° ex: Ler 10 números, armazenar em um vetor, calcular a soma e a média, e exibir os valores

#include <stdio.h>
#include <string.h>

int main() {
    .
    int m = 0; // Variável para armazenar a média
    int s = 0; // Variável para armazenar a soma dos valores
    int vet[10]; // Declaração de um vetor de 10 posições [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    
    // Laço para ler os 10 valores inseridos pelo usuário
    for (int i = 0; i < 10; i++) { 
        printf("Digite o valor %d valor: ", i + 1);
        scanf("%d", &vet[i]); // Armazena o valor na posição 'i' do vetor
        s += vet[i]; // Acumula o valor lido na variável de soma
    }
    
    // Cálculo da média aritmética inteira
    m = s / 10;
    
    // Exibição dos resultados globais
    printf("Valor da soma %d\n", s);
    printf("Valor da media: %d\n", m);
    printf("Valor do vetor [vet] = ");
    
    // Laço para exibir todos os elementos armazenados no vetor
    for (int i = 0; i < 10; i++) {
        printf("[%d]", vet[i]);
    }
    
    return 0;
}

# 2 ex: Ler 10 números, encontrar o maior e o menor valor, e registrar suas respectivas posições (índices).

#include <stdio.h>

int main() {
    
    int maior_valor = 0; // Armazena o maior número encontrado
    int menor_valor = 0; // Armazena o menor número encontrado
    int pos_maior = 0;   // Guarda a posição (índice) do maior valor
    int pos_menor = 0;   // Guarda a posição (índice) do menor valor
    int vet[10];         // Vetor com capacidade para 10 inteiros

    for (int i = 0; i < 10; i++) {
        printf("Digite o %d valor: ", i + 1);
        scanf("%d", &vet[i]);

        // Na primeira iteração, inicializa o maior e menor com o primeiro elemento digitado
        if (i == 0) {
            maior_valor = vet[i];
            menor_valor = vet[i];
            pos_maior = i;
            pos_menor = i;
        }

        // Atualiza o maior valor e sua posição se encontrar um número maior
        if (vet[i] > maior_valor) {
            maior_valor = vet[i];
            pos_maior = i;
        }

        // Atualiza o menor valor e sua posição se encontrar um número menor
        if (vet[i] < menor_valor) {
            menor_valor = vet[i];
            pos_menor = i;
        }
    }

    // Exibe os resultados finais
    printf("O maior valor e %d, na posicao %d\n", maior_valor, pos_maior);
    printf("O menor valor e %d, na posicao %d\n", menor_valor, pos_menor);

    return 0;
}

# 3 ex: Ler 20 números, filtrar e exibir apenas os pares, contar quantos são e somá-los.

#include <stdio.h>

int main() {
    
    int vet[20]; // Vetor para armazenar 20 números
    int c = 0;   // Contador de números pares
    int s = 0;   // Acumulador da soma dos números pares
    
    // Leitura dos 20 valores do vetor
    for (int i = 0; i < 20; i++) {
        printf("Qual valor para a %d posição? ", i + 1); 
        scanf("%d", &vet[i]);
    }
    
    printf("Pares: ");

    // Varre o vetor para identificar e processar os números pares
    for (int i = 0; i < 20; i++) {
        // Verifica se o resto da divisão por 2 é zero (número par)
        if (vet[i] % 2 == 0) {
            c += 1;          // Incrementa o contador de pares
            s += vet[i];     // Soma o número par encontrado
            printf("[%d]", vet[i]); // Exibe o número par
        }
    }
    
    // Exibição das estatísticas finais dos pares
    printf("\nQuantidade de números pares: %d\n", c);
    printf("A soma dos números pares é de: %d\n", s);
    
    return 0;
}

# 4 ex: Ler 10 valores em um vetor e exibi-los tanto na ordem original quanto na ordem invertida.

#include <stdio.h>

int main() {
    
    int vet[10]; // Vetor de 10 posições

    // Leitura dos 10 valores
    for (int i = 0; i < 10; i++) {
        printf("Qual o %d valor: ", i + 1);
        scanf("%d", &vet[i]);
    }
    
    // Exibição do vetor na ordem original
    printf("Vetor normal: ");
    for (int i = 0; i < 10; i++) {
        printf("[%d] ", vet[i]);
    }
    
    // Exibição do vetor na ordem invertida (começando do índice 9 até 0)
    printf("\nVetor invertido: ");
    for (int i = 9; i >= 0; i--) {
        printf("[%d] ", vet[i]);
    }
    
    return 0;
}

# 5 ex: Preencher uma matriz 3x3, calcular a soma total de seus elementos e encontrar o maior valor.

#include <stdio.h>

int main() {
    
    int s = 0;         // Acumulador para a soma de todos os elementos
    int mat[3][3];     // Matriz de 3 linhas e 3 colunas
    int maior = 0;     // Variável para rastrear o maior valor
    
    // Laço duplo para preencher a matriz 3x3
    for (int i = 0; i <= 2; i++) {
        for (int j = 0; j <= 2; j++) {
            printf("Qual o valor para a posição [%d][%d]: ", i, j);
            scanf("%d", &mat[i][j]);
        }
    }
    
    printf("Matriz: \n");
    // Laço duplo para percorrer, exibir e processar os dados da matriz
    for (int i = 0; i <= 2; i++) {
        for (int j = 0; j <= 2; j++) {
            s += mat[i][j];   // Soma cada elemento ao total geral
            
            // Na primeira iteração assume o valor atual como maior, depois compara
            if (i == 0 && j == 0) {
                maior = mat[i][j];
            } else if (mat[i][j] > maior) {
                maior = mat[i][j]; // Atualiza o maior valor encontrado
            }
            
            printf("[%d] ", mat[i][j]);
        }
        printf("\n"); // Quebra de linha ao fim de cada linha da matriz
    }
    
    // Exibição dos resultados finais
    printf("Soma dos valores da matriz: %d\n", s);
    printf("O maior valor da matriz: %d\n", maior);
    
    return 0;
}

#6 ex: Ler uma matriz 4x4, exibir seus elementos e isolar a diagonal principal calculando sua soma.

#include <stdio.h>

int main() {
    
    int s = 0;         // Soma dos elementos da diagonal principal
    int mat[4][4];     // Matriz quadrada 4x4

    // Leitura dos dados da matriz
    for (int i = 0; i <= 3; i++) {
        for (int j = 0; j <= 3; j++) {
            printf("Qual o valor para a posição [%d][%d]: ", i, j);
            scanf("%d", &mat[i][j]);
        }
    }
    
    // Exibição da matriz completa
    printf("Matriz completa: \n");
    for (int i = 0; i <= 3; i++) {
        for (int j = 0; j <= 3; j++) {
            printf(" [%d] ", mat[i][j]);
        }
        printf("\n");
    }
    
    // Extração e cálculo da diagonal principal
    printf("Diagonal principal: \n");
    for (int i = 0; i <= 3; i++) {
        int j = i; // Na diagonal principal, linha e coluna são iguais
        s += mat[i][j]; // Acumula o valor da diagonal
        printf("[%d]", mat[i][j]);
    }
    
    printf("\nTotal dos valores da diagonal principal: %d\n", s); 

    return 0;
}

#7 ex: Usar uma matriz 4x3 para armazenar 3 notas de 4 alunos e calcular a média de cada estudante.

#include <stdio.h>

int main() {
    
    int s;
    int m = 0;
    int mat[4][3]; // Matriz 4x3 (4 alunos e 3 notas cada)

    // Preenchendo a matriz com as notas
    for (int i = 0; i < 4; i++) {
        for (int j = 0; j < 3; j++) {
            printf("Qual a %d nota do %d aluno: ", j + 1, i + 1);
            scanf("%d", &mat[i][j]);
        }
    }

    // Calculando a média de cada aluno individualmente
    for (int i = 0; i < 4; i++) {
        s = 0;  // Reinicia a soma para cada novo aluno

        for (int j = 0; j < 3; j++) {
            s += mat[i][j]; // Soma as 3 notas do aluno atual
        }

        m = s / 3; // Calcula a média inteira

        printf("A media do aluno %d e: %d\n", i + 1, m);
    }

    return 0;
}

#8 ex: Cadastrar 5 produtos usando struct, calcular o valor total em estoque de cada um e achar o maior.
#include <stdio.h>

// Definição da estrutura para representar um Produto
struct Produto {
    char nome[50];
    int codigo;
    float preco;
    int quantidade;
};

int main() {
    struct Produto produtos[5]; // Vetor de struct para 5 produtos

    // Cadastro dos produtos via teclado
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

    // Cálculo do valor total em estoque para cada produto e identificação do maior
    for (int i = 0; i < 5; i++) {
        float valor_total = produtos[i].preco * produtos[i].quantidade;

        printf("\nProduto: %s\n", produtos[i].nome);
        printf("Codigo: %d\n", produtos[i].codigo);
        printf("Preco: %.2f\n", produtos[i].preco);
        printf("Quantidade: %d\n", produtos[i].quantidade);
        printf("Valor total em estoque: %.2f\n", valor_total);

        // Verifica se este produto tem o maior valor total acumulado
        if (valor_total > maior_valor) {
            maior_valor = valor_total;
            pos_maior = i;
        }
    }

    // Exibição do destaque de maior valor em estoque
    printf("\n===== MAIOR VALOR EM ESTOQUE =====\n");
    printf("Produto: %s\n", produtos[pos_maior].nome);
    printf("Valor em estoque: %.2f\n", maior_valor);

    return 0;
}

#9 ex: Cadastrar 5 alunos com struct, calcular suas médias, contar aprovados/reprovados e achar a maior média.

#include <stdio.h>

// Definição da estrutura do Aluno
struct Aluno {
    char nome[50];
    int idade;
    float nota1;
    float nota2;
    float nota3;
};

int main() {
    struct Aluno alunos[5]; // Vetor de 5 alunos

    int aprovados = 0;
    int reprovados = 0;

    float maior_media = 0;
    int pos_maior = 0;

    // Cadastro dos dados dos alunos
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

    // Processamento das notas e cálculo das médias
    for (int i = 0; i < 5; i++) {
        float media = (alunos[i].nota1 +
                       alunos[i].nota2 +
                       alunos[i].nota3) / 3;

        printf("\nAluno: %s", alunos[i].nome);
        printf("\nMedia: %.2f", media);

        // Critério de aprovação (média >= 7.0)
        if (media >= 7.0) {
            printf("\nStatus: Aprovado");
            aprovados++;
        } else {
            printf("\nStatus: Reprovado");
            reprovados++;
        }

        // Rastreamento da maior média da turma
        if (media > maior_media) {
            maior_media = media;
            pos_maior = i;
        }
    }

    // Exibição do sumário estatístico final
    printf("\n\n===== RESULTADO FINAL =====\n");
    printf("Aprovados: %d\n", aprovados);
    printf("Reprovados: %d\n", reprovados);
    printf("Aluno com maior media: %s\n", alunos[pos_maior].nome);
    printf("Maior media: %.2f\n", maior_media);

    return 0;
}

#10 ex: Criar um menu interativo com struct para gerenciar funcionários, listar dados, calcular médias e maior salário.

#include <stdio.h>

// Definição da estrutura Funcionario
struct Funcionario {
    char nome[50];
    int idade;
    char cargo[50];
    float salario;
};

int main() {
    struct Funcionario funcionarios[10]; // Vetor para até 10 funcionários
    int opcao;

    // Loop do menu principal que executa até o usuário escolher sair (opção 0)
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

        // Opção 1: Cadastro dos dados
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
        // Opção 2: Listagem de todos os funcionários cadastrados
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
        // Opção 3: Identificação do maior salário da empresa
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
        // Opção 4: Cálculo da média salarial da equipe
        else if (opcao == 4) {
            float soma = 0;
            float media;

            for (int i = 0; i < 10; i++) {
                soma += funcionarios[i].salario;
            }

            media = soma / 10;
            printf("\nMedia salarial: %.2f\n", media);
        }
        // Opção 5: Listagem de funcionários que recebem acima da média salarial
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