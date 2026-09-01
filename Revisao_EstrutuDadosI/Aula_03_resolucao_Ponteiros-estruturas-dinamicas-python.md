# Exercícios e Respostas — Ponteiros, Referências e Estruturas Dinâmicas

---

## Exercício 1 — Referências

**Enunciado:**
Execute o código abaixo:
```python
a = [10, 20, 30]
b = a

b.append(40)

print("a:", a)
print("b:", b)
print("id(a):", id(a))
print("id(b):", id(b))
```

**Responda:**
1. Qual será a saída? 
**R=** Tanto a variável a, quanto a b, aparecerão os números de 10, 20, 30, 40, enquanto o ID será o mesmo, pois no python, ID retorna a idadentidade do objeto e b passou a receber a identidade de a.

**Saída esperada:**
```text
a: [10, 20, 30, 40]
b: [10, 20, 30, 40]
id(a): 139926715091264 (exemplo de ID)
id(b): 139926715091264 (mesmo ID de 'a')
```

2. `a` e `b` representam o mesmo objeto? 
**R=** a e b representam o mesmo objeto.

3. Por quê? 
**R=** Já que um passou a receber a referência do mesmo objeto.

4. O que aconteceria com `b = a.copy()`? 
**R=** b receberia uma cópia de a, logo b ainda referenciaria ele mesmo, depois do append, b teria o 40 adicionado ao final, enquanto a teria somente o 30 no final.

---

## Exercício 2 — Construindo uma cadeia

**Enunciado:**
Crie:
```python
n1 = Node("A")
n2 = Node("B")
n3 = Node("C")
```
Conecte (`A → B → C → None`) e depois percorra a estrutura produzindo a saída A, B e C.

**Resposta:**
```python
class Node:
    def __init__(self, valor):
        self.valor = valor
        self.proximo = None

n1 = Node("A")
n2 = Node("B")
n3 = Node("C")

n1.proximo = n2
n2.proximo = n3

atual = n1

while (atual != None):
    print(f"{atual.valor} -->")
    atual = atual.proximo

print(atual)
```

**Saída esperada:**
```text
A -->
B -->
C -->
None
```

---

## Exercício 3 — Depuração

**Enunciado:**
Analise o código:
```python
n1 = Node(10)
n2 = Node(20)
n3 = Node(30)

n1.proximo = n2
n2.proximo = n3

atual = n1

while atual is not None:
    print(atual.valor)
```

**Perguntas:**
1. Qual é o problema? 
**R=** O número 10 fica repetindo no LOOP.

2. Por que o programa não termina? 
**R=** A variável atual sempre valerá o valor atual, nunca pegando o valor de proximo, e nunca chegando no ponto de parada do While que é quando atual vale None.

3. Qual linha deve ser acrescentada? 
**R=** 
```python
atual = atual.proximo
print(atual)
```

4. Qual será a saída depois da correção? 
**R=** 10, 20, 30, None.

**Saída esperada (após a correção):**
```text
10
20
30
None
```

---

## Problema real — Sistema de atendimento de uma clínica

**Enunciado:**
Uma clínica recebe pacientes durante o dia. Cada paciente possui: nome, idade e prioridade.
O sistema deve permitir:
1. adicionar paciente;
2. listar pacientes;
3. atender o primeiro paciente;
4. verificar se a fila está vazia;
5. informar a quantidade de pacientes.

**Exemplo de utilização:**
```python
fila = FilaAtendimento()

fila.adicionar(Paciente("Ana", 32, "Normal"))
fila.adicionar(Paciente("Bruno", 70, "Prioridade"))
fila.adicionar(Paciente("Carlos", 45, "Normal"))

fila.listar()

paciente = fila.atender()
print("Atendendo:", paciente.nome)
```

**Resposta:**
```python
class Paciente:
    def __init__(self, nome, idade, prioridade):
        self.nome = nome
        self.idade = idade
        self.prioridade = prioridade

class Node:
    def __init__(self, paciente):
        self.paciente = paciente
        self.proximo = None

class FilaAtendimento:
    def __init__(self):
        self.inicio = None
        self.fim = None
        self._tamanho = 0

    def esta_vazia(self):
        return self.inicio is None

    def tamanho(self):
        return self._tamanho

    def adicionar(self, paciente):
        novo_no = Node(paciente)
        
        # Se a fila estiver vazia, o novo nó é tanto o início quanto o fim
        if self.esta_vazia():
            self.inicio = novo_no
            self.fim = novo_no
        else:
            # O antigo fim agora aponta para o novo nó
            self.fim.proximo = novo_no
            # O ponteiro de fim da fila se atualiza para o novo nó
            self.fim = novo_no
            
        self._tamanho += 1

    def atender(self):
        if self.esta_vazia():
            print("A fila está vazia!")
            return None

        # Guardamos o paciente do início para retornar
        paciente_atendido = self.inicio.paciente

        # O início pula para o próximo da fila
        self.inicio = self.inicio.proximo
        self._tamanho -= 1

        # Se após atender a fila ficou vazia, o fim também deve ser None
        if self.inicio is None:
            self.fim = None

        return paciente_atendido

    def listar(self):
        if self.esta_vazia():
            print("Fila vazia.")
            return

        atual = self.inicio
        print("\n--- ESTADO DA FILA ---")
        while atual is not None:
            p = atual.paciente
            print(f"{p.nome} — {p.idade} anos — {p.prioridade}")
            atual = atual.proximo
        print("----------------------\n")


# ==========================================
# Exemplo de utilização (conforme o enunciado)
# ==========================================
fila = FilaAtendimento()

fila.adicionar(Paciente("Ana", 32, "Normal"))
fila.adicionar(Paciente("Bruno", 70, "Prioridade"))
fila.adicionar(Paciente("Carlos", 45, "Normal"))

fila.listar()

print(f"Quantidade de pacientes na fila: {fila.tamanho()}")

paciente = fila.atender()
print("Atendendo:", paciente.nome)

print(f"Quantidade de pacientes após o atendimento: {fila.tamanho()}")

fila.listar()
```

**Saída esperada:**
```text
--- ESTADO DA FILA ---
Ana — 32 anos — Normal
Bruno — 70 anos — Prioridade
Carlos — 45 anos — Normal
----------------------

Quantidade de pacientes na fila: 3
Atendendo: Ana
Quantidade de pacientes após o atendimento: 2

--- ESTADO DA FILA ---
Bruno — 70 anos — Prioridade
Carlos — 45 anos — Normal
----------------------
```

---

## Desafio — Atendimento prioritário

**Enunciado:**
Amplie o sistema. Pacientes com prioridade devem ser atendidos antes dos pacientes normais.

**Resposta:**
```python
class Paciente:
    def __init__(self, nome, idade, prioridade):
        self.nome = nome
        self.idade = idade
        self.prioridade = prioridade  # Ex: "Normal" ou "Prioridade"

class Node:
    def __init__(self, paciente):
        self.paciente = paciente
        self.proximo = None

class FilaAtendimentoPrioritaria:
    def __init__(self):
        self.inicio = None
        self.fim = None
        self._tamanho = 0

    def esta_vazia(self):
        return self.inicio is None

    def tamanho(self):
        return self._tamanho

    def adicionar(self, paciente):
        novo_no = Node(paciente)
        
        # Caso 1: Fila vazia
        if self.esta_vazia():
            self.inicio = novo_no
            self.fim = novo_no
            
        # Caso 2: O novo paciente tem PRIORIDADE
        elif paciente.prioridade.lower() == "prioridade":
            # Subcaso A: O primeiro da fila já NÃO é prioritário, 
            # então o novo prioritário assume o trono (vira o novo início).
            if self.inicio.paciente.prioridade.lower() != "prioridade":
                novo_no.proximo = self.inicio
                self.inicio = novo_no
            else:
                # Subcaso B: Procurar o último nó que ainda é prioritário
                atual = self.inicio
                while atual.proximo is not None and atual.proximo.paciente.prioridade.lower() == "prioridade":
                    atual = atual.proximo
                
                # Inserir o novo nó entre o 'atual' e o 'atual.proximo'
                novo_no.proximo = atual.proximo
                atual.proximo = novo_no
                
                # Se por acaso ele parou no fim da fila, atualizamos o ponteiro self.fim
                if novo_no.proximo is None:
                    self.fim = novo_no
                    
        # Caso 3: O novo paciente é NORMAL (entra no fim padrão)
        else:
            self.fim.proximo = novo_no
            self.fim = novo_no
            
        self._tamanho += 1

    def atender(self):
        if self.esta_vazia():
            print("A fila está vazia!")
            return None

        paciente_atendido = self.inicio.paciente
        self.inicio = self.inicio.proximo
        self._tamanho -= 1

        if self.inicio is None:
            self.fim = None

        return paciente_atendido

    def listar(self):
        if self.esta_vazia():
            print("Fila vazia.")
            return

        atual = self.inicio
        print("\n--- ESTADO DA FILA (COM PRIORIDADE) ---")
        posicao = 1
        while atual is not None:
            p = atual.paciente
            print(f"{posicao}. {p.nome} — {p.idade} anos — [{p.prioridade}]")
            atual = atual.proximo
            posicao += 1
        print("---------------------------------------\n")
```

**Saída esperada (se adicionarmos Ana, Bruno e Carlos conforme o enunciado):**
```text
--- ESTADO DA FILA (COM PRIORIDADE) ---
1. Carlos — 45 anos — [Prioridade]
2. Ana — 32 anos — [Normal]
3. Bruno — 70 anos — [Normal]
---------------------------------------
```

---

## Trabalho colaborativo

**Enunciado:**
Forme um grupo de 2 a 4 estudantes. Modele, implemente, teste e depure. Encontre e corrija pelo menos um erro proposital.

**Resposta:**
```python
class Paciente:
    def __init__(self, nome, idade, prioridade):
        self.nome = nome
        self.idade = idade
        self.prioridade = prioridade  # "Normal" ou "Prioridade"


class Node:
    def __init__(self, paciente):
        self.paciente = paciente
        self.proximo = None


class FilaAtendimento:
    def __init__(self):
        self.inicio = None
        self.fim = None
        self._tamanho = 0

    def esta_vazia(self):
        return self.inicio is None

    def tamanho(self):
        return self._tamanho

    def adicionar(self, paciente):
        novo_no = Node(paciente)

        # 1. Fila totalmente vazia
        if self.esta_vazia():
            self.inicio = novo_no
            self.fim = novo_no

        # 2. Paciente com PRIORIDADE
        elif paciente.prioridade.lower() == "prioridade":
            # Se o primeiro da fila NÃO for prioritário, o novo entra na cabeça da fila
            if self.inicio.paciente.prioridade.lower() != "prioridade":
                novo_no.proximo = self.inicio
                self.inicio = novo_no
            else:
                # Caminha até achar o último prioritário ou o fim da fila
                atual = self.inicio
                while atual.proximo is not None and atual.proximo.paciente.prioridade.lower() == "prioridade":
                    atual = atual.proximo

                novo_no.proximo = atual.proximo
                atual.proximo = novo_no

                # ERRO PROPOSITAL CORRIGIDO (veja a Etapa 4 abaixo!)
                if novo_no.proximo is None:
                    self.fim = novo_no

        # 3. Paciente NORMAL (vai para o fim)
        else:
            self.fim.proximo = novo_no
            self.fim = novo_no

        self._tamanho += 1

    def atender(self):
        if self.esta_vazia():
            return None

        paciente_atendido = self.inicio.paciente
        self.inicio = self.inicio.proximo
        self._tamanho -= 1

        # Se esvaziou a fila inteira, o fim também precisa virar None!
        if self.inicio is None:
            self.fim = None

        return paciente_atendido

    def listar(self):
        if self.esta_vazia():
            print("Fila vazia.")
            return

        atual = self.inicio
        while atual is not None:
            p = atual.paciente
            print(f"- {p.nome} [{p.prioridade}]")
            atual = atual.proximo
```

**Saída esperada (se testado com 5 pacientes variados e listar no final):**
```text
- Carlos [Prioridade]
- Maria [Prioridade]
- Ana [Normal]
- Bruno [Normal]
- Joao [Normal]
```

---

## Exercício de revisão — Sistema de atendimento

**Enunciado:**
Desenvolva individualmente uma versão funcional.
Checklist:
- [x] Criar `Paciente`;
- [x] Criar `Node`;
- [x] Criar `FilaAtendimento`;
- [x] Implementar `adicionar()`;
- [x] Implementar `atender()`;
- [x] Implementar `listar()`;
- [x] Implementar `esta_vazia()`;
- [x] Implementar `tamanho()`;
- [x] Testar pelo menos cinco pacientes;
- [x] Documentar um erro encontrado e sua correção.

---

## Reflexão final

### O que é uma referência em Python?
**R=** Quando alguma variável é referenciada por outro, ou seja, quando ela passa a apontar para o mesmo objeto.

### Qual a diferença entre `b = a` e `b = a.copy()`?
**R=** Uma é referência e a outra é cópia.

### Por que uma estrutura encadeada precisa de referências?
**R=** Para nunca perder os valores próximos, sempre ter algum referencial de qual vai ser o próximo valor.

### Qual erro você encontrou durante a depuração?
**R=** Erros como passar a referência errada.

### Como referências ajudam a compreender estruturas dinâmicas?
**R=** Que o valor atual sempre vai mudando até que atual seja None.