"""
test_red_black_forest.py
-------------------------
Testes de sanidade:
  1. Após inserir N chaves aleatórias com fixup completo, a árvore
     satisfaz as 5 propriedades formais da Rubro-Negra.
  2. O motor declara vitória quando todas as inserções são corrigidas.
  3. O motor força o colapso (degeneração em corrente) quando o
     jogador erra sistematicamente as correções.
"""

import random

from rbtree import RedBlackForest
from game_engine import CrowForestGame, GameConfig, GameOverError


def test_red_black_invariants_hold_after_many_inserts():
    rng = random.Random(7)
    keys = rng.sample(range(1, 5000), 500)
    tree = RedBlackForest()
    for k in keys:
        path = tree.insert(k)
        tree.fixup_chain(path[-1])

    assert tree.is_valid_red_black_tree(), "Propriedades RN violadas após fixup completo"
    # busca continua log(n): altura não deve degenerar
    import math
    assert tree.height() <= 2 * math.log2(len(keys) + 1) + 2


def test_perfect_player_wins():
    game = CrowForestGame(config=GameConfig(total_chicks=15))
    rng = random.Random(1)
    pool = rng.sample(range(1, 1000), 15)
    for k in pool:
        game.play_round(k)
    assert game.won
    assert game.tree.is_valid_red_black_tree()


def test_bad_player_causes_collapse():
    game = CrowForestGame(
        config=GameConfig(total_chicks=50, violation_limit=2),
        resolve_action=lambda action: False,  # sempre erra
    )
    rng = random.Random(2)
    pool = rng.sample(range(1, 1000), 50)
    collapsed = False
    try:
        for k in pool:
            game.play_round(k)
    except GameOverError:
        collapsed = True

    assert collapsed
    assert game.lost
    assert game.tree.is_degenerate_chain() or game.tree.height() == game.tree.size


if __name__ == "__main__":
    test_red_black_invariants_hold_after_many_inserts()
    test_perfect_player_wins()
    test_bad_player_causes_collapse()
    print("Todos os testes passaram.")
