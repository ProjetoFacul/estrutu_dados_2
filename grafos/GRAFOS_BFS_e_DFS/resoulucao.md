# Grafos, BFS e DFS — Simulação de contingência de rede

**Disciplina:** Estrutura de Dados II — Ciência da Computação
**Estudo de caso:** pane relacionada ao GPS e impactos em voos no Aeroporto de Brasília (G1, 22 set. 2026)

> **Aviso:** simulação computacional didática. A notícia apenas motiva o problema; as conexões e os bloqueios são **fictícios** e não representam rotas aéreas reais nem servem para orientar navegação ou voos.

## Conteúdo da entrega
| Arquivo | Descrição |
|---|---|
| `solucao_grafos.py` | Implementação executável (lista de adjacência, BFS, DFS, bloqueios, testes) |
| `README.md` | Este documento |
| `diagrama_grafo.png` | Diagrama do grafo (manter na mesma pasta do README) |
| `evidencia_demo.txt`, `evidencia_testes.txt`, `evidencia_interativo.txt` | Saídas reais das execuções |

## Como executar
```bash
python solucao_grafos.py            # modo interativo: origem, destino e bloqueios
python solucao_grafos.py --demo     # cenários prontos de contingência
python solucao_grafos.py --testes   # 15 testes automáticos
```
Requer apenas Python 3 (biblioteca padrão).

---

# 8. Desafio individual: desenvolvimento da solução

## 8.1 Pergunta de pesquisa computacional
> **Na rede simulada, quantas conexões precisam ficar indisponíveis para que Brasília deixe de alcançar Curitiba, e como BFS e DFS se comportam a cada bloqueio?**

**Objetivo:** modelar a rede como grafo, implementar BFS e DFS, simular bloqueios sem alterar a rede original e comparar os caminhos encontrados.

**Hipótese:** como Curitiba tem 5 conexões e Brasília apenas 2, a rede resiste a qualquer bloqueio isolado, e o ponto fraco está nas duas saídas de Brasília.

**Resultado:** a hipótese se confirmou. Nenhuma conexão sozinha isola o par (teste T15); bastam **2** conexões (Brasília–Goiânia e Brasília–Belo Horizonte), valor obtido por força bruta (corte mínimo).

## 8.2 Grafo (≥ 7 vértices) e conexões justificadas
G = (V, E) **não dirigido** e **não ponderado**, com |V| = 9 e |E| = 13.

![Diagrama do grafo](diagrama_grafo.png)

*A aresta vermelha tracejada é o bloqueio Goiânia–São Paulo (Cenário B).*

| Conexão | Justificativa (hipotética) |
|---|---|
| Brasília–Goiânia, Brasília–Belo Horizonte | Brasília é o hub de origem e tem duas saídas, uma para o Centro-Oeste e outra para o Sudeste |
| Goiânia–São Paulo, Goiânia–Campo Grande | Ligações do Centro-Oeste ao Sudeste e ao corredor Oeste |
| Belo Horizonte–Rio de Janeiro, Belo Horizonte–São Paulo, São Paulo–Rio de Janeiro | Malha do Sudeste, que forma um ciclo e cria rotas alternativas |
| São Paulo–Curitiba, Rio de Janeiro–Curitiba, Campo Grande–Curitiba | Três entradas para o destino principal, vindas de regiões diferentes |
| Curitiba–Florianópolis, Curitiba–Porto Alegre, Florianópolis–Porto Alegre | Malha do Sul, com outro ciclo, usada para testar caminhos mais longos |

**Grau dos vértices:** Curitiba 5, São Paulo 4, Goiânia 3, Belo Horizonte 3, Rio de Janeiro 3, Brasília 2, Campo Grande 2, Florianópolis 2, Porto Alegre 2.

## 8.3 Implementação: lista de adjacência, BFS e DFS
- **Lista de adjacência:** dicionário cujas chaves são cidades e cujos valores são listas de vizinhos (`construir_grafo`). Como o grafo é não dirigido, cada aresta aparece nos dois extremos.
- **BFS:** fila FIFO (`deque`), marca visitados ao enfileirar e retorna o primeiro caminho que chega ao destino, que tem o menor número de arestas.
- **DFS:** pilha LIFO, marca visitados ao desempilhar. Os vizinhos são empilhados em ordem reversa para que a primeira cidade da lista seja explorada primeiro.
- **Complexidade:** O(V + E) para a exploração com lista de adjacência. Como cada item da fila/pilha guarda uma cópia do caminho (`caminho + [vizinho]`), o custo prático é maior em grafos grandes; uma melhoria seria guardar apenas o predecessor de cada vértice e reconstruir o caminho no final.

Código-fonte completo (`solucao_grafos.py`):

```python
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
```

**Saída do programa** (`python solucao_grafos.py --demo`):
```text
Vértices: 9 | Arestas: 13

=== Cenário A — rede íntegra ===
BFS: Brasília → Goiânia → São Paulo → Curitiba  [3 aresta(s)]
DFS: Brasília → Goiânia → São Paulo → Belo Horizonte → Rio de Janeiro → Curitiba  [5 aresta(s)]
  -> DFS achou um caminho 2 aresta(s) mais longo que o BFS.

=== Cenário B — bloqueio Goiânia–São Paulo ===
BFS: Brasília → Goiânia → Campo Grande → Curitiba  [3 aresta(s)]
DFS: Brasília → Goiânia → Campo Grande → Curitiba  [3 aresta(s)]

=== Cenário C — Goiânia–São Paulo + Campo Grande–Curitiba ===
BFS: Brasília → Belo Horizonte → Rio de Janeiro → Curitiba  [3 aresta(s)]
DFS: Brasília → Belo Horizonte → Rio de Janeiro → São Paulo → Curitiba  [4 aresta(s)]
  -> DFS achou um caminho 1 aresta(s) mais longo que o BFS.

=== Cenário D — Brasília isolada (as duas saídas bloqueadas) ===
BFS: sem caminho no modelo
DFS: sem caminho no modelo

=== Cenário E — Brasília → Porto Alegre ===
BFS: Brasília → Goiânia → São Paulo → Curitiba → Porto Alegre  [4 aresta(s)]
DFS: Brasília → Goiânia → São Paulo → Belo Horizonte → Rio de Janeiro → Curitiba → Florianópolis → Porto Alegre  [7 aresta(s)]
  -> DFS achou um caminho 3 aresta(s) mais longo que o BFS.

=== Cenário F — mesma rede, vizinhos em ordem invertida ===
BFS: Brasília → Belo Horizonte → São Paulo → Curitiba  [3 aresta(s)]
DFS: Brasília → Belo Horizonte → São Paulo → Curitiba  [3 aresta(s)]

=== Bloqueio de UMA conexão por vez (Brasília → Curitiba) ===
Conexão bloqueada                   BFS  DFS
Belo Horizonte – Brasília             3    5
Belo Horizonte – Rio de Janeiro       3    4
Belo Horizonte – São Paulo            3    4
Brasília – Goiânia                    3    6
Campo Grande – Curitiba               3    5
Campo Grande – Goiânia                3    5
Curitiba – Florianópolis              3    5
Curitiba – Porto Alegre               3    5
Curitiba – Rio de Janeiro             3    3
Curitiba – São Paulo                  3    5
Florianópolis – Porto Alegre          3    5
Goiânia – São Paulo                   3    3
Rio de Janeiro – São Paulo            3    5

Pergunta de pesquisa: bastam 2 conexões bloqueadas para isolar Brasília de Curitiba.
Exemplo de corte mínimo: [('Belo Horizonte', 'Brasília'), ('Brasília', 'Goiânia')]
Grafo original preservado após todas as simulações.
```

## 8.4 Entrada do usuário e validação de nomes
No modo interativo, `pedir_cidade()` repete a pergunta enquanto o nome não existir na rede e lista as cidades válidas. A comparação ignora maiúsculas, minúsculas e acentos (`brasilia` equivale a `Brasília`). Os bloqueios informados também são validados: nomes inválidos e conexões que não existem são recusados.

Exemplo real (trecho da execução, completa em 8.8):
```text
Origem: atlantis
  Cidade inexistente na rede. Opções: Belo Horizonte, Brasília, Campo Grande, ...
Origem: brasilia
```

## 8.5 Bloqueio de aresta sem alterar a rede original
`bloquear_conexoes(rede, bloqueios)` cria uma **cópia** das listas de adjacência e remove a aresta nos dois sentidos. O dicionário `GRAFO` nunca é modificado: o `--demo` termina com um `assert` que compara a rede com a original, e os testes T6 e T7 verificam a preservação e a remoção nos dois sentidos.

## 8.6 Caminhos, quantidade de arestas e casos sem caminho
Cada resultado é impresso no formato `A → B → C [n aresta(s)]`. Quando não há caminho, as buscas retornam `None` e o programa escreve "sem caminho no modelo", sem erro.

**Cenários (Brasília → Curitiba):**

| Cenário | BFS | DFS |
|---|---|---|
| A — rede íntegra | Brasília → Goiânia → São Paulo → Curitiba (**3**) | Brasília → Goiânia → São Paulo → Belo Horizonte → Rio de Janeiro → Curitiba (**5**) |
| B — bloqueio Goiânia–São Paulo | Brasília → Goiânia → Campo Grande → Curitiba (**3**) | igual ao BFS (**3**) |
| C — B + Campo Grande–Curitiba | Brasília → Belo Horizonte → Rio de Janeiro → Curitiba (**3**) | Brasília → Belo Horizonte → Rio de Janeiro → São Paulo → Curitiba (**4**) |
| D — Brasília–Goiânia e Brasília–Belo Horizonte bloqueadas | **sem caminho** | **sem caminho** |
| E — Brasília → Porto Alegre (rede íntegra) | 4 arestas | 7 arestas |
| F — rede íntegra com vizinhos em ordem invertida | Brasília → Belo Horizonte → São Paulo → Curitiba (**3**) | igual ao BFS (**3**) |

**Bloqueio de uma conexão por vez (Brasília → Curitiba):**

| Conexão bloqueada | BFS | DFS |
|---|:-:|:-:|
| Belo Horizonte – Brasília | 3 | 5 |
| Belo Horizonte – Rio de Janeiro | 3 | 4 |
| Belo Horizonte – São Paulo | 3 | 4 |
| Brasília – Goiânia | 3 | 6 |
| Campo Grande – Curitiba | 3 | 5 |
| Campo Grande – Goiânia | 3 | 5 |
| Curitiba – Florianópolis | 3 | 5 |
| Curitiba – Porto Alegre | 3 | 5 |
| Curitiba – Rio de Janeiro | 3 | 3 |
| Curitiba – São Paulo | 3 | 5 |
| Florianópolis – Porto Alegre | 3 | 5 |
| Goiânia – São Paulo | 3 | 3 |
| Rio de Janeiro – São Paulo | 3 | 5 |

**Leitura:** o BFS permanece em 3 arestas em todos os casos, porque existem quatro caminhos de 3 arestas entre Brasília e Curitiba (via Goiânia–São Paulo, Goiânia–Campo Grande, Belo Horizonte–São Paulo e Belo Horizonte–Rio de Janeiro), e nenhum bloqueio isolado elimina todos. O DFS oscila entre 3 e 6, pois depende do ramo que explora primeiro.

## 8.7 Comparação BFS × DFS e limitações

| Aspecto | BFS | DFS |
|---|---|---|
| Estrutura | Fila (FIFO) | Pilha (LIFO) ou recursão |
| Estratégia | Explora por níveis, dos vizinhos mais próximos aos mais distantes | Aprofunda um ramo antes de voltar |
| Caminho obtido | Menor número de arestas (grafo não ponderado) | Um caminho qualquer, sem garantia de ser curto |
| Dependência da ordem dos vizinhos | Não altera o tamanho do caminho | Pode mudar o caminho (Cenários A × F) |
| Existe caminho? | Sim, decide corretamente | Sim, decide corretamente (Cenário D) |
| Complexidade | O(V + E) | O(V + E) |
| Observado | 3 arestas em todos os testes de Brasília → Curitiba | 3 a 6 arestas; 7 no Cenário E |

**Limitações da solução**
- O grafo **não tem pesos**: "menor" significa menos arestas, não menor tempo, distância, combustível ou custo (para isso, Dijkstra; Gomes, cap. 7).
- Não há direção, horários, capacidade, escalas, clima nem regras aeronáuticas.
- Os bloqueios são hipóteses didáticas, sem relação comprovada com a pane noticiada.
- A rede é pequena e inventada, e os resultados não se generalizam para a malha real.
- O corte mínimo por força bruta cresce exponencialmente com o número de arestas; em redes grandes usa-se fluxo máximo.
- Guardar o caminho completo em cada item da fila/pilha gasta memória extra; guardar predecessores seria mais eficiente.

## 8.8 Implementação funcionando e testes executados

### Cenários (`python solucao_grafos.py --demo`)
A saída completa está na seção 8.3, logo abaixo do código-fonte.

### Testes automáticos (`python solucao_grafos.py --testes`)
```text
[OK] T1 grafo simétrico (cada aresta nos dois extremos)
[OK] T2 pelo menos 7 vértices
[OK] T3 BFS: Brasília→Curitiba com 3 arestas
[OK] T4 DFS retorna caminho válido
[OK] T5 DFS ≥ BFS em nº de arestas
[OK] T6 original intacto após bloqueio
[OK] T7 bloqueio remove nos dois sentidos
[OK] T8 BFS ainda encontra caminho após bloqueio B
[OK] T9 BFS e DFS retornam None sem caminho
[OK] T10 origem == destino → caminho de 0 arestas
[OK] T11 validação aceita 'brasilia' e rejeita 'Atlantis'
[OK] T12 BFS nunca é mais longo que DFS (todos os pares)
[OK] T13 corte mínimo Brasília–Curitiba = 2
[OK] T14 inverter vizinhos muda o caminho do DFS
[OK] T15 nenhum bloqueio único desconecta Brasília de Curitiba

15/15 testes passaram.
```

### Modo interativo (`python solucao_grafos.py`)
Entradas digitadas: `atlantis` (inválida, rejeitada), `brasilia`, `curitiba`, bloqueios `goiania`–`sao paulo` e `brasilia`–`belo horizonte`, depois ENTER.
```text
SIMULAÇÃO DIDÁTICA — não representa rotas reais.

Cidades: Belo Horizonte, Brasília, Campo Grande, Curitiba, Florianópolis, Goiânia, Porto Alegre, Rio de Janeiro, São Paulo
Origem:   Cidade inexistente na rede. Opções: Belo Horizonte, Brasília, Campo Grande, Curitiba, Florianópolis, Goiânia, Porto Alegre, Rio de Janeiro, São Paulo
Origem: Destino: 
=== Rede íntegra ===
BFS: Brasília → Goiânia → São Paulo → Curitiba  [3 aresta(s)]
DFS: Brasília → Goiânia → São Paulo → Belo Horizonte → Rio de Janeiro → Curitiba  [5 aresta(s)]
  -> DFS achou um caminho 2 aresta(s) mais longo que o BFS.

Informe conexões a bloquear (ENTER vazio para terminar).
  Bloquear — cidade 1:   Bloquear — cidade 2:   Bloqueada: Goiânia–São Paulo
  Bloquear — cidade 1:   Bloquear — cidade 2:   Bloqueada: Brasília–Belo Horizonte
  Bloquear — cidade 1: 
=== Rede com bloqueios: Goiânia–São Paulo, Brasília–Belo Horizonte ===
BFS: Brasília → Goiânia → Campo Grande → Curitiba  [3 aresta(s)]
DFS: Brasília → Goiânia → Campo Grande → Curitiba  [3 aresta(s)]
```

## Entregáveis
- [x] `solucao_grafos.py` executável
- [x] `README.md` com problema, objetivo, instruções, estrutura do grafo e resultados
- [x] Diagrama do grafo (`diagrama_grafo.png`) e evidências dos testes (`evidencia_*.txt`)
- [x] Roteiro de apresentação de 5 minutos (abaixo)

## Critérios de avaliação (10 pontos): onde cada um é atendido
| Critério | Pontos | Onde |
|---|:-:|---|
| Modelagem do problema e grafo | 2,0 | 8.1 e 8.2 |
| Implementação correta de BFS e DFS | 3,0 | 8.3 e testes T3, T4, T12 |
| Simulação e testes de contingência | 2,0 | 8.5, 8.6 e 8.8 |
| Comparação crítica e limitações | 1,5 | 8.7 |
| Organização e apresentação da solução | 1,5 | Estrutura deste README e roteiro abaixo |

## Roteiro sugerido para a apresentação (5 minutos)
| Tempo | O que mostrar |
|---|---|
| 0:00–0:45 | Contexto: a notícia motiva o problema, mas a rede é fictícia. Apresentar a pergunta de pesquisa |
| 0:45–1:45 | Diagrama do grafo, as 13 conexões e a justificativa de cada região |
| 1:45–2:30 | Código: lista de adjacência, fila no BFS, pilha no DFS e o conjunto de visitados |
| 2:30–4:00 | Demonstração ao vivo: `--demo` (Cenários A, B e D) e um exemplo interativo com nome inválido |
| 4:00–4:40 | Comparação: BFS sempre com 3 arestas e DFS variando de 3 a 6; efeito da ordem dos vizinhos |
| 4:40–5:00 | Conclusão: bastam 2 bloqueios; limitações (sem pesos, modelo não operacional) |

---

# 9. Questões para reflexão

**1. Por que um grafo representa melhor a rede de conexões do que uma árvore binária?**
Uma árvore binária não admite ciclos, tem um único caminho entre dois nós e limita cada nó a dois filhos. Uma rede de conexões tem vértices com graus variados (Curitiba tem 5), ciclos (Belo Horizonte–São Paulo–Rio de Janeiro) e rotas alternativas, que são justamente o que a simulação de bloqueio explora. Só um grafo representa isso.

**2. Em qual condição BFS encontra o menor caminho? O que significa "menor"?**
Em grafos **não ponderados** (ou com pesos todos iguais), porque o BFS visita os vértices em ordem crescente de número de arestas a partir da origem. "Menor" significa **menos arestas**, e não menor distância, tempo ou custo. Na simulação, o BFS achou 3 arestas em todos os cenários com caminho.

**3. Por que DFS pode retornar um caminho diferente de BFS?**
O DFS segue um ramo até esgotá-lo antes de voltar, e o primeiro caminho que encontra depende da ordem dos vizinhos. No Cenário A ele deu uma volta de 5 arestas (passando por Belo Horizonte e Rio de Janeiro) enquanto o BFS fez 3. Inverter as listas de vizinhos (Cenário F) mudou o caminho do DFS sem mudar o grafo.

**4. O que ocorre se não utilizarmos um conjunto de visitados?**
Em um grafo com ciclos, o algoritmo volta a vértices já explorados: o laço pode não terminar ou a fila/pilha cresce sem parar, e a complexidade deixa de ser O(V + E). Aqui, por exemplo, Brasília → Goiânia → Brasília → Goiânia... se repetiria indefinidamente, pois a aresta é bidirecional.

**5. Quais informações adicionais seriam necessárias para avaliar tempo ou custo de uma rota?**
Pesos nas arestas (distância, duração do voo, tarifa, combustível), horários e frequência dos voos, tempo mínimo de conexão, capacidade das aeronaves e dos aeroportos, condições meteorológicas e restrições operacionais. Com pesos não negativos, o algoritmo adequado seria Dijkstra, e não BFS/DFS.

**6. Por que o resultado do algoritmo não pode ser usado para orientar um voo real?**
Porque as cidades, as conexões e os bloqueios são fictícios e o modelo ignora segurança, regulação, espaço aéreo, tipo de aeronave, combustível, clima e janelas de horário. A navegação aérea exige dados oficiais e sistemas certificados, e o grafo só responde sobre conectividade em um modelo simplificado.

---

## Referências
GOMES, Paulo César Rodacki. *Grafos: conceitos fundamentais, algoritmos e aplicações*. Blumenau: Editora IFC, 2022. ISBN 978-65-88089-12-5. (Capítulos 1, 2, 3 e 7.)

G1 DISTRITO FEDERAL. *Pane em GPS afeta voos da Azul no Aeroporto de Brasília; passageiros reclamam de atrasos*. 22 set. 2026.
