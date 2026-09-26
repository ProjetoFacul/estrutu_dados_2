# Como executar o projeto Bosque dos Corvos

Este guia explica, passo a passo, como rodar todas as partes do projeto: a simulação em Python (motor de jogo, árvore rubro-negra, telemetria e testes) e o jogo jogável em HTML.

## O que compõe o projeto

| Arquivo | Papel |
|---|---|
| `rbtree.py` | A árvore rubro-negra em si: inserção, detecção de violação, ações de correção, rotações e verificação das 5 propriedades. |
| `game_engine.py` | O motor de jogo: aplica o core loop (pouso → travessia → correção → equilíbrio de sombra → pressão crescente) sobre a árvore. |
| `telemetry.py` | Pipeline de dados local em SQLite: grava eventos de partida e calcula estatísticas agregadas por fase. |
| `demo.py` | Script de demonstração: roda uma partida detalhada e um lote de partidas simuladas, imprimindo os resultados. |
| `test_red_black_forest.py` | Testes de sanidade: valida as propriedades da árvore, o caminho de vitória e o caminho de colapso. |
| `bosque-dos-corvos.html` | O jogo jogável no navegador (versão independente, em JavaScript). |

## Pré-requisitos

- **Python 3.9 ou mais recente** instalado. Verifique com:

```bash
python3 --version
```

- Nenhuma biblioteca externa é necessária — o projeto usa apenas a biblioteca padrão do Python (`sqlite3`, `dataclasses`, `random`, etc.).
- Para o jogo em HTML, basta um navegador (Chrome, Firefox, Edge, Safari); não é preciso instalar nada.

## Passo 1 — Baixe os arquivos em uma mesma pasta

Coloque `rbtree.py`, `game_engine.py`, `telemetry.py`, `demo.py` e `test_red_black_forest.py` **na mesma pasta**. Os módulos se importam uns aos outros pelo nome do arquivo (`from rbtree import ...`, `from game_engine import ...`), então isso só funciona se todos estiverem lado a lado.

```
minha-pasta/
├── rbtree.py
├── game_engine.py
├── telemetry.py
├── demo.py
└── test_red_black_forest.py
```

## Passo 2 — Rode a demonstração completa

Dentro da pasta, execute:

```bash
python3 demo.py
```

Isso vai:

1. Imprimir o log rodada a rodada de uma partida "perfeita" (um jogador que sempre acerta a ação de correção);
2. Simular 30 partidas por fase, em 5 fases, com jogadores que erram com taxas variadas;
3. Criar um arquivo `crow_forest_telemetry.db` (banco SQLite) na mesma pasta, com o histórico de todas as sessões simuladas;
4. Imprimir uma tabela `LEVEL_STATS` com taxa de conclusão, melhor pontuação, médias e percentis por fase.

Se quiser inspecionar o banco gerado diretamente:

```bash
sqlite3 crow_forest_telemetry.db "select * from game_sessions limit 10;"
```

(o comando `sqlite3` já vem com a maioria dos sistemas; se não tiver, é só apagar o `.db` e rodar `demo.py` de novo quando precisar dele).

## Passo 3 — Rode os testes

```bash
python3 test_red_black_forest.py
```

Um resultado correto termina com:

```
Todos os testes passaram.
```

Os três testes verificam, nessa ordem:

- que, após 500 inserções aleatórias com correção automática, a árvore satisfaz as 5 propriedades formais da árvore rubro-negra e sua altura continua próxima de log₂(n);
- que um jogador que sempre acerta consegue vencer a partida (todos os filhotes acomodados, árvore válida);
- que um jogador que sempre erra provoca o colapso do bosque (degeneração em uma corrente linear).

Se preferir usar `pytest` (opcional, não é necessário):

```bash
pip install pytest --break-system-packages
pytest test_red_black_forest.py -v
```

## Passo 4 — Use o motor em um script próprio

Para jogar uma partida programaticamente, sem passar pelo `demo.py`:

```python
from game_engine import CrowForestGame, GameConfig, GameOverError

# resolve_action é a "jogada" — aqui, um oráculo que sempre acerta.
# Troque a função por uma que decide de outra forma para simular
# um jogador real (por exemplo, lendo uma entrada do teclado).
jogo = CrowForestGame(config=GameConfig(total_chicks=12))

for chave in [8, 3, 15, 1, 5, 12, 20, 4, 7, 14, 18, 25]:
    try:
        log = jogo.play_round(chave)
        print(log)
    except GameOverError as erro:
        print("Fim de jogo:", erro)
        break

print(jogo.summary())
```

## Passo 5 — Abra o jogo jogável (HTML)

O arquivo `bosque-dos-corvos.html` é a versão jogável no navegador, independente do código Python (a lógica da árvore foi reescrita em JavaScript dentro do próprio arquivo). Para rodá-lo:

- **Mais simples:** dê duplo clique no arquivo, ou arraste-o para uma aba do navegador.
- **Alternativa:** clique no link do artefato publicado no chat — ele abre direto, sem precisar baixar nada.

Não é necessário nenhum servidor, build ou instalação: é um único arquivo autocontido.

## Solução de problemas comuns

| Sintoma | Causa provável | Solução |
|---|---|---|
| `ModuleNotFoundError: No module named 'rbtree'` | Os arquivos não estão na mesma pasta, ou você rodou o script de outro diretório. | Rode `python3 demo.py` estando dentro da pasta onde os `.py` estão, ou ajuste o `PYTHONPATH`. |
| `ValueError: Chave X já existe no bosque` | Você tentou inserir uma chave repetida na árvore. | Use chaves únicas a cada `insert`/`play_round` (o `demo.py` já faz isso embaralhando um `range`). |
| Banco `crow_forest_telemetry.db` com dados antigos misturados | O arquivo é reaproveitado entre execuções. | Apague o `.db` antes de rodar `demo.py` de novo, se quiser um histórico limpo. |
| O jogo HTML não abre / tela em branco | Bloqueio de JavaScript no navegador, ou arquivo baixado incompleto. | Habilite JavaScript para arquivos locais ou abra o link do artefato publicado em vez do arquivo baixado. |

## Resumo dos comandos

```bash
python3 demo.py                      # simulação completa + telemetria
python3 test_red_black_forest.py     # testes de sanidade
sqlite3 crow_forest_telemetry.db     # (opcional) inspecionar o banco gerado
```
