"""
game_engine.py
--------------
Motor do "Bosque dos Corvos" (upgrade Rubro-Negra do "The Hanoi Tree").

Implementa fielmente o Core Loop do GDD (seção 4.4):

  1. Um novo filhote pousa (inserção, sempre vermelho).
  2. O jogador percorre a árvore comparando até achar a posição (BST).
  3. Tio vermelho -> "Repintar Ninho"; tio preto/ausente -> "Realocar
     Galho" (rotação simples/dupla) + recoloração.
  4. Recalcula-se a altura preta de cada ramo; alturas iguais rendem
     pontos de "equilíbrio de sombra".
  5. Repete-se, com o intervalo entre pousos diminuindo (pressão).

Condição de vitória: N filhotes acomodados com a propriedade
rubro-negra válida em toda a árvore.

Condição de derrota: violações de cor não corrigidas se acumulam além
de `violation_limit` -> o bosque colapsa (degenera em lista, O(n)).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Callable

from rbtree import RedBlackForest, FixupAction


@dataclass
class RoundLog:
    round_no: int
    chick_key: int
    path_len: int
    actions_applied: List[str]
    points_gained: int
    spawn_interval_ms: int
    shade_balanced_after: bool


@dataclass
class GameConfig:
    total_chicks: int = 12          # N do GDD: quantos filhotes precisam pousar
    initial_interval_ms: int = 3000
    min_interval_ms: int = 700
    interval_decay: float = 0.90    # pousos ficam mais rápidos a cada rodada
    violation_limit: int = 3        # correções erradas/perdidas toleradas
    points_per_action: int = 10
    shade_bonus: int = 25           # "equilíbrio de sombra"
    win_multiplier: float = 1.5


class GameOverError(Exception):
    """Levantado quando o bosque colapsa (condição de derrota)."""


class CrowForestGame:
    """
    `resolve_action` é injetável — em produção seria o clique do
    jogador na UI (repintar_ninho / realocar_galho); aqui, por padrão,
    usa um oráculo que sempre acerta (útil para testes/telemetria),
    mas pode receber uma função que simula erros/acertos de um
    jogador real.
    """

    def __init__(
        self,
        config: Optional[GameConfig] = None,
        resolve_action: Optional[Callable[[FixupAction], bool]] = None,
    ) -> None:
        self.config = config or GameConfig()
        self.tree = RedBlackForest()
        self.round_no = 0
        self.score = 0
        self.uncorrected_violations = 0
        self.spawn_interval_ms = self.config.initial_interval_ms
        self.logs: List[RoundLog] = []
        self.won = False
        self.lost = False
        # oráculo padrão: sempre escolhe a ação correta
        self._resolve_action = resolve_action or (lambda action: True)

    # ------------------------------------------------------------------ #
    def play_round(self, key: int) -> RoundLog:
        if self.won or self.lost:
            raise GameOverError("A partida já terminou.")

        self.round_no += 1

        # 1) pouso + 2) travessia comparativa (posição via BST)
        path = self.tree.insert(key)
        new_node = path[-1]

        actions_applied: List[str] = []
        cur = new_node
        while cur is not None and self.tree.has_violation(cur):
            required = self.tree.required_action(cur)
            player_correct = self._resolve_action(required)

            if player_correct:
                cur = self.tree.apply_action(cur, required)
                actions_applied.append(required.kind)
                self.score += self.config.points_per_action
            else:
                # jogador errou/não agiu a tempo -> violação fica sem correção
                self.uncorrected_violations += 1
                if self.uncorrected_violations >= self.config.violation_limit:
                    self.tree.collapse_to_chain()
                    self.lost = True
                    break
                # o bosque ainda precisa ficar consistente para o próximo
                # pouso: o motor aplica a correção "à força" (o galho
                # racha, mas não derruba o jogo ainda), sem premiar pontos.
                cur = self.tree.apply_action(cur, required)

        self.tree.root.color = self.tree.root and self.tree.root.color  # no-op guard
        if self.tree.root is not None:
            from rbtree import Color
            self.tree.root.color = Color.BLACK

        # 4) equilíbrio de sombra
        shade_ok = self.tree.is_shade_balanced()
        if shade_ok and not self.lost:
            self.score += self.config.shade_bonus

        log = RoundLog(
            round_no=self.round_no,
            chick_key=key,
            path_len=len(path),
            actions_applied=actions_applied,
            points_gained=self.config.points_per_action * len(actions_applied)
            + (self.config.shade_bonus if shade_ok and not self.lost else 0),
            spawn_interval_ms=self.spawn_interval_ms,
            shade_balanced_after=shade_ok,
        )
        self.logs.append(log)

        # 5) pressão crescente
        self.spawn_interval_ms = max(
            self.config.min_interval_ms,
            int(self.spawn_interval_ms * self.config.interval_decay),
        )

        if self.lost:
            raise GameOverError(
                f"O bosque colapsou na rodada {self.round_no}: "
                f"{self.uncorrected_violations} violações não corrigidas. "
                f"Altura final degenerada: {self.tree.height()} "
                f"(esperado ~log2({self.tree.size}))."
            )

        if self.tree.size >= self.config.total_chicks and self.tree.is_valid_red_black_tree():
            self.won = True
            self.score = int(self.score * self.config.win_multiplier)

        return log

    # ------------------------------------------------------------------ #
    def summary(self) -> dict:
        return {
            "rounds": self.round_no,
            "score": self.score,
            "won": self.won,
            "lost": self.lost,
            "tree_size": self.tree.size,
            "tree_height": self.tree.height(),
            "valid_rb_tree": self.tree.is_valid_red_black_tree(),
            "uncorrected_violations": self.uncorrected_violations,
            "final_spawn_interval_ms": self.spawn_interval_ms,
        }
