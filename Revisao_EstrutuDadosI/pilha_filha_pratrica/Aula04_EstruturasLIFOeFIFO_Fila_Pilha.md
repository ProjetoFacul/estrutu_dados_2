# Compilação de Algoritmos em Python — Pilhas e Filas

---

# Exercício 1 — Editor de Texto com Pilha (Desfazer/Undo)

**Enunciado:**
Implemente uma estrutura de dados de Pilha (`LIFO` - Last In, First Out) aplicada a um editor de texto simples para simular a funcionalidade de "Desfazer" (`Undo`), permitindo executar ações, desfazê-las e visualizar o histórico.

**Resposta:**
class EditorDeTexto:
    def __init__(self):
        # A pilha que armazenará as ações
        self.pilha_desfazer = []

    def executar_acao(self, acao):
        \"\"\"Adiciona uma nova ação no topo da pilha.\"\"\"
        self.pilha_desfazer.append(acao)
        print(f"Ação executada: {acao}")

    def desfazer(self):
        \"\"\"Remove e reverte estritamente o último comando inserido (LIFO).\"\"\"
        if len(self.pilha_desfazer) > 0:
            acao_removida = self.pilha_desfazer.pop()
            print(f"Desfazendo a ação: {acao_removida}")
        else:
            print("Nenhuma ação para desfazer!")

    def ver_historico(self):
        print(f"Pilha atual (base -> topo): {self.pilha_desfazer}")


# --- Exemplo de uso ---
editor = EditorDeTexto()

editor.executar_acao("Digitar 'Olá'")
editor.executar_acao("Digitar ' mundo'")
editor.executar_acao("Apagar ' mundo'")

print("\n--- Acionando o 'Desfazer' ---")
editor.desfazer()  # Vai remover e desfazer a última ação ("Apagar ' mundo'")
editor.desfazer()  # Vai remover e desfazer a penúltima ação ("Digitar ' mundo'")

**Saída esperada:**
Ação executada: Digitar 'Olá'
Ação executada: Digitar ' mundo'
Ação executada: Apagar ' mundo'

--- Acionando o 'Desfazer' ---
Desfazendo a ação: Apagar ' mundo'
Desfazendo a ação: Digitar ' mundo'

---

# Exercício 2 — Spooler de Impressão com Fila (FIFO)

**Enunciado:**
Implemente uma estrutura de dados de Fila (`FIFO` - First In, First Out) utilizando `deque` para simular um gerenciador de fila de impressão (Spooler), permitindo enfileirar documentos, imprimi-los na ordem correta e visualizar a fila de espera.

**Resposta:**
from collections import deque

class SpoolerImpressao:
    def __init__(self):
        # deque é perfeito para filas, pois tirar do começo é instantâneo
        self.fila = deque()

    def enfileirar(self, documento):
        \"\"\"Adiciona um novo documento no final da fila.\"\"\"
        self.fila.append(documento)
        print(f"📥 Documento recebido: '{documento}' (Aguardando...)")

    def imprimir(self):
        \"\"\"Imprime e remove o documento mais antigo (FIFO).\"\"\"
        if len(self.fila) > 0:
            # popleft() tira o primeirão da fila
            doc_atual = self.fila.popleft()
            print(f"🖨️ Imprimindo agora: '{doc_atual}'")
        else:
            print("📭 Fila vazia! Nada para imprimir no momento.")

    def ver_fila(self):
        \"\"\"Mostra como a fila está no momento.\"\"\"
        print(f"Fila atual: {list(self.fila)}")


# --- Testando a Impressora ---
impressora = SpoolerImpressao()

# Mandando documentos (Enqueue)
impressora.enfileirar("Trabalho_de_Sistemas.pdf")
impressora.enfileirar("Boleto_Faculdade.pdf")
impressora.enfileirar("Resumo_Provas.docx")

print("\n--- Iniciando os trabalhos ---")
# Imprimindo (Dequeue)
impressora.imprimir() # Vai imprimir o Trabalho_de_Sistemas (mais antigo)
impressora.imprimir() # Vai imprimir o Boleto
impressora.ver_fila() # Vai mostrar que só sobrou o Resumo

**Saída esperada:**
📥 Documento recebido: 'Trabalho_de_Sistemas.pdf' (Aguardando...)
📥 Documento recebido: 'Boleto_Faculdade.pdf' (Aguardando...)
📥 Documento recebido: 'Resumo_Provas.docx' (Aguardando...)

--- Iniciando os trabalhos ---
🖨️ Imprimindo agora: 'Trabalho_de_Sistemas.pdf'
🖨️ Imprimindo agora: 'Boleto_Faculdade.pdf'
Fila atual: ['Resumo_Provas.docx']