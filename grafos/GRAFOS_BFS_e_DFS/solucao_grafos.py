"""
Solução do desafio individual — Grafos, BFS e DFS (Estrutura de Dados II)

Pergunta de pesquisa:
    Na rede simulada, quantas conexões precisam ficar indisponíveis para que
    Brasília deixe de alcançar Curitiba, e como BFS e DFS reagem a cada bloqueio?

ATENÇÃO: simulação didática. Conexões e bloqueios são fictícios e NÃO
representam rotas aéreas reais nem orientam navegação operacional.

Uso:
    python solucao_grafos.py            # modo interativo
    python solucao_grafos.py --demo     # cenários prontos (evidências)
    python solucao_grafos.py --testes   # testes automáticos
"""
import sys
import unicodedata
from collections import deque
from itertools import combinations

# ---------------------------------------------------------------------------
# 1. Modelagem: grafo NÃO dirigido em lista de adjacência (dicionário)
# ---------------------------------------------------------------------------
ARESTAS = [
    ("Brasília", "Goiânia"),
    ("Brasília", "Belo Horizonte"),
    ("Goiânia", "São Paulo"),
    ("Goiânia", "Campo Grande"),
    ("Belo Horizonte", "Rio de Janeiro"),
    ("Belo Horizonte", "São Paulo"),
    ("São Paulo", "Rio de Janeiro"),
    ("São Paulo", "Curitiba"),
    ("Rio de Janeiro", "Curitiba"),
    ("Campo Grande", "Curitiba"),
    ("Curitiba", "Florianópolis"),
    ("Curitiba", "Porto Alegre"),
    ("Florianópolis", "Porto Alegre"),
]


def construir_grafo(arestas):
    """Cria a lista de adjacência; cada aresta aparece nos dois extremos."""
    rede = {}
    for a, b in arestas:
        rede.setdefault(a, []).append(b)
        rede.setdefault(b, []).append(a)
    return rede


GRAFO = construir_grafo(ARESTAS)


# ---------------------------------------------------------------------------
# 2. Algoritmos de busca
# ---------------------------------------------------------------------------
def bfs(rede, origem, destino):
    """Busca em largura (fila FIFO). Menor nº de arestas em grafo não ponderado."""
    fila = deque([(origem, [origem])])
    visitados = {origem}
    while fila:
        atual, caminho = fila.popleft()
        if atual == destino:
            return caminho
        for vizinho in rede.get(atual, []):
            if vizinho not in visitados:
                visitados.add(vizinho)
                fila.append((vizinho, caminho + [vizinho]))
    return None


def dfs(rede, origem, destino):
    """Busca em profundidade (pilha LIFO). Acha um caminho, não necessariamente o menor."""
    pilha = [(origem, [origem])]
    visitados = set()
    while pilha:
        atual, caminho = pilha.pop()
        if atual in visitados:
            continue
        visitados.add(atual)
        if atual == destino:
            return caminho
        for vizinho in reversed(rede.get(atual, [])):  # mantém a ordem da lista
            if vizinho not in visitados:
                pilha.append((vizinho, caminho + [vizinho]))
    return None


# ---------------------------------------------------------------------------
# 3. Contingência (nunca altera o grafo original)
# ---------------------------------------------------------------------------
def bloquear_conexoes(rede, bloqueios):
    """Devolve uma CÓPIA da rede sem as arestas listadas (nos dois sentidos)."""
    copia = {no: vizinhos.copy() for no, vizinhos in rede.items()}
    for a, b in bloqueios:
        if b in copia.get(a, []):
            copia[a].remove(b)
        if a in copia.get(b, []):
            copia[b].remove(a)
    return copia


def conexoes_minimas_para_desconectar(rede, origem, destino):
    """Responde à pergunta de pesquisa por força bruta: menor conjunto de
    arestas cuja remoção desconecta origem de destino (corte mínimo)."""
    arestas = sorted({tuple(sorted((a, b))) for a in rede for b in rede[a]})
    for k in range(1, len(arestas) + 1):
        for combo in combinations(arestas, k):
            if bfs(bloquear_conexoes(rede, combo), origem, destino) is None:
                return k, list(combo)
    return None, []


def analisar_bloqueios_unicos(rede, origem, destino):
    """Bloqueia UMA aresta por vez e registra o efeito em BFS e DFS."""
    arestas = sorted({tuple(sorted((a, b))) for a in rede for b in rede[a]})
    linhas = []
    for a, b in arestas:
        nova = bloquear_conexoes(rede, [(a, b)])
        linhas.append(((a, b), bfs(nova, origem, destino), dfs(nova, origem, destino)))
    return linhas


# ---------------------------------------------------------------------------
# 4. Utilidades de entrada/saída
# ---------------------------------------------------------------------------
def _norm(txt):
    """Ignora acentos, maiúsculas e espaços extras ('brasilia' == 'Brasília')."""
    s = unicodedata.normalize("NFD", txt.strip().lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


def resolver_cidade(rede, texto):
    """Devolve o nome oficial do vértice ou None se não existir."""
    for no in rede:
        if _norm(no) == _norm(texto):
            return no
    return None


def formatar(caminho):
    if caminho is None:
        return "sem caminho no modelo"
    return f"{' → '.join(caminho)}  [{len(caminho) - 1} aresta(s)]"


def comparar(rede, origem, destino, titulo):
    print(f"\n=== {titulo} ===")
    pb, pd = bfs(rede, origem, destino), dfs(rede, origem, destino)
    print("BFS:", formatar(pb))
    print("DFS:", formatar(pd))
    if pb and pd and len(pd) > len(pb):
        print(f"  -> DFS achou um caminho {len(pd) - len(pb)} aresta(s) mais longo que o BFS.")
    return pb, pd


# ---------------------------------------------------------------------------
# 5. Modos de execução
# ---------------------------------------------------------------------------
def demo():
    o, d = "Brasília", "Curitiba"
    print("Vértices:", len(GRAFO), "| Arestas:", len(ARESTAS))
    comparar(GRAFO, o, d, "Cenário A — rede íntegra")
    comparar(bloquear_conexoes(GRAFO, [("Goiânia", "São Paulo")]), o, d,
             "Cenário B — bloqueio Goiânia–São Paulo")
    comparar(bloquear_conexoes(GRAFO, [("Goiânia", "São Paulo"), ("Campo Grande", "Curitiba")]),
             o, d, "Cenário C — Goiânia–São Paulo + Campo Grande–Curitiba")
    comparar(bloquear_conexoes(GRAFO, [("Brasília", "Goiânia"), ("Brasília", "Belo Horizonte")]),
             o, d, "Cenário D — Brasília isolada (as duas saídas bloqueadas)")
    comparar(GRAFO, "Brasília", "Porto Alegre", "Cenário E — Brasília → Porto Alegre")

    # Experimento D: ordem dos vizinhos altera o DFS sem alterar o grafo
    invertida = {no: list(reversed(v)) for no, v in GRAFO.items()}
    comparar(invertida, o, d, "Cenário F — mesma rede, vizinhos em ordem invertida")

    print(f"\n=== Bloqueio de UMA conexão por vez ({o} → {d}) ===")
    print(f"{'Conexão bloqueada':<34}{'BFS':>5}{'DFS':>5}")
    for (a, b), pb, pd in analisar_bloqueios_unicos(GRAFO, o, d):
        nb = len(pb) - 1 if pb else "—"
        nd = len(pd) - 1 if pd else "—"
        print(f"{a + ' – ' + b:<34}{nb:>5}{nd:>5}")

    k, corte = conexoes_minimas_para_desconectar(GRAFO, o, d)
    print(f"\nPergunta de pesquisa: bastam {k} conexões bloqueadas para isolar {o} de {d}.")
    print("Exemplo de corte mínimo:", corte)
    assert GRAFO == construir_grafo(ARESTAS), "o grafo original foi alterado!"
    print("Grafo original preservado após todas as simulações.")


def testes():
    o, d = "Brasília", "Curitiba"
    resultados = []

    def checar(nome, cond):
        resultados.append(cond)
        print(f"[{'OK' if cond else 'FALHOU'}] {nome}")

    # T1 — simetria do grafo não dirigido
    checar("T1 grafo simétrico (cada aresta nos dois extremos)",
           all(a in GRAFO[b] for a in GRAFO for b in GRAFO[a]))
    # T2 — mínimo de 7 vértices
    checar("T2 pelo menos 7 vértices", len(GRAFO) >= 7)
    # T3 — BFS acha caminho com menor nº de arestas (3)
    checar("T3 BFS: Brasília→Curitiba com 3 arestas", len(bfs(GRAFO, o, d)) - 1 == 3)
    # T4 — DFS acha um caminho válido
    pd = dfs(GRAFO, o, d)
    valido = pd and pd[0] == o and pd[-1] == d and all(
        b in GRAFO[a] for a, b in zip(pd, pd[1:]))
    checar("T4 DFS retorna caminho válido", bool(valido))
    # T5 — DFS pode ser mais longo que BFS
    checar("T5 DFS ≥ BFS em nº de arestas", len(pd) >= len(bfs(GRAFO, o, d)))
    # T6 — bloqueio não altera o original
    copia = bloquear_conexoes(GRAFO, [("Goiânia", "São Paulo")])
    checar("T6 original intacto após bloqueio", "São Paulo" in GRAFO["Goiânia"])
    checar("T7 bloqueio remove nos dois sentidos",
           "São Paulo" not in copia["Goiânia"] and "Goiânia" not in copia["São Paulo"])
    # T8 — ainda há caminho após 1 bloqueio
    checar("T8 BFS ainda encontra caminho após bloqueio B", bfs(copia, o, d) is not None)
    # T9 — sem caminho tratado com None
    isolada = bloquear_conexoes(GRAFO, [("Brasília", "Goiânia"), ("Brasília", "Belo Horizonte")])
    checar("T9 BFS e DFS retornam None sem caminho",
           bfs(isolada, o, d) is None and dfs(isolada, o, d) is None)
    # T10 — origem == destino
    checar("T10 origem == destino → caminho de 0 arestas", bfs(GRAFO, o, o) == [o])
    # T11 — validação de nomes
    checar("T11 validação aceita 'brasilia' e rejeita 'Atlantis'",
           resolver_cidade(GRAFO, "brasilia") == "Brasília"
           and resolver_cidade(GRAFO, "Atlantis") is None)
    # T12 — BFS é ótimo: compara com todas as origens/destinos
    def comp(c):
        return len(c) - 1
    ok = True
    for x in GRAFO:
        for y in GRAFO:
            b, p = bfs(GRAFO, x, y), dfs(GRAFO, x, y)
            if comp(b) > comp(p):
                ok = False
    checar("T12 BFS nunca é mais longo que DFS (todos os pares)", ok)
    # T13 — corte mínimo
    checar("T13 corte mínimo Brasília–Curitiba = 2",
           conexoes_minimas_para_desconectar(GRAFO, o, d)[0] == 2)
    # T14 — ordem dos vizinhos muda DFS mas não BFS em tamanho
    inv = {no: list(reversed(v)) for no, v in GRAFO.items()}
    checar("T14 inverter vizinhos muda o caminho do DFS",
           dfs(GRAFO, o, d) != dfs(inv, o, d))

    # T15 — nenhuma aresta isolada desconecta Brasília de Curitiba
    checar("T15 nenhum bloqueio único desconecta Brasília de Curitiba",
           all(pb is not None and pd is not None
               for _, pb, pd in analisar_bloqueios_unicos(GRAFO, o, d)))

    print(f"\n{sum(resultados)}/{len(resultados)} testes passaram.")
    return all(resultados)


def pedir_cidade(rede, rotulo):
    while True:
        texto = input(f"{rotulo}: ")
        cidade = resolver_cidade(rede, texto)
        if cidade:
            return cidade
        print("  Cidade inexistente na rede. Opções:", ", ".join(sorted(rede)))


def interativo():
    print("SIMULAÇÃO DIDÁTICA — não representa rotas reais.\n")
    print("Cidades:", ", ".join(sorted(GRAFO)))
    origem = pedir_cidade(GRAFO, "Origem")
    destino = pedir_cidade(GRAFO, "Destino")
    comparar(GRAFO, origem, destino, "Rede íntegra")

    bloqueios = []
    print("\nInforme conexões a bloquear (ENTER vazio para terminar).")
    while True:
        a = input("  Bloquear — cidade 1: ").strip()
        if not a:
            break
        b = input("  Bloquear — cidade 2: ").strip()
        ca, cb = resolver_cidade(GRAFO, a), resolver_cidade(GRAFO, b)
        if not ca or not cb:
            print("  Nome inválido.")
        elif cb not in GRAFO[ca]:
            print("  Essa conexão não existe na rede.")
        else:
            bloqueios.append((ca, cb))
            print(f"  Bloqueada: {ca}–{cb}")
    if bloqueios:
        comparar(bloquear_conexoes(GRAFO, bloqueios), origem, destino,
                 "Rede com bloqueios: " + ", ".join(f"{a}–{b}" for a, b in bloqueios))


if __name__ == "__main__":
    if "--demo" in sys.argv:
        demo()
    elif "--testes" in sys.argv:
        sys.exit(0 if testes() else 1)
    else:
        interativo()
