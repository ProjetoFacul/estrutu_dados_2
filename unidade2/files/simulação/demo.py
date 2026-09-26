"""
demo.py
-------
Simula várias "sessões" do Bosque dos Corvos (o upgrade Rubro-Negra do
The Hanoi Tree) e alimenta o pipeline de telemetria, imprimindo:

  1. o log rodada-a-rodada de uma partida vencida;
  2. um lote de partidas simuladas com uma taxa de erro do jogador
     configurável, para gerar dados de telemetria realistas;
  3. as estatísticas agregadas por fase (level_stats), como as que
     alimentariam o painel de administração do jogo original.

Rodar:  python demo.py
"""

from __future__ import annotations

import random
import time

from game_engine import CrowForestGame, GameConfig, GameOverError
from rbtree import FixupAction
from telemetry import TelemetryStore


def make_player(error_rate: float, rng: random.Random):
    """Oráculo de jogador: acerta a ação correta com prob. (1 - error_rate)."""

    def resolve(action: FixupAction) -> bool:
        return rng.random() >= error_rate

    return resolve


def play_one_session(store: TelemetryStore, level: int, error_rate: float, seed: int) -> None:
    rng = random.Random(seed)
    config = GameConfig(total_chicks=10, violation_limit=3)
    game = CrowForestGame(config=config, resolve_action=make_player(error_rate, rng))

    store.log_start(level)
    key_pool = list(range(1, 300))
    rng.shuffle(key_pool)

    t0 = time.monotonic()
    used_keys = 0
    try:
        for key in key_pool:
            if game.won:
                break
            game.play_round(key)
            used_keys += 1
    except GameOverError:
        pass

    elapsed = int(time.monotonic() - t0) or rng.randint(5, 40)  # simulado, sessão é instantânea
    summary = game.summary()

    if summary["won"]:
        store.log_complete(
            level=level,
            moves=summary["rounds"],
            time_seconds=elapsed,
            actions_created=used_keys,
        )
    else:
        store.log_abandon(
            level=level,
            moves=summary["rounds"],
            time_seconds=elapsed,
            actions_created=used_keys,
        )


def print_verbose_game() -> None:
    print("=" * 70)
    print("PARTIDA DETALHADA — jogador perfeito (oráculo sempre acerta)")
    print("=" * 70)
    game = CrowForestGame(config=GameConfig(total_chicks=8))
    keys = [15, 7, 24, 3, 11, 20, 30, 9]
    for k in keys:
        log = game.play_round(k)
        acoes = ", ".join(log.actions_applied) or "— (sem violação)"
        print(
            f"Rodada {log.round_no:>2} | filhote #{log.chick_key:<3} | "
            f"ações: {acoes:<45} | dossel equilibrado: {log.shade_balanced_after} | "
            f"pontos: +{log.points_gained} | próximo pouso em {log.spawn_interval_ms}ms"
        )
    print("-" * 70)
    print("Resumo final:", game.summary())
    print()


def print_stats(store: TelemetryStore) -> None:
    print("=" * 70)
    print("LEVEL_STATS — agregação de telemetria (pipeline de dados)")
    print("=" * 70)
    header = (
        f"{'Fase':>4} | {'starts':>6} | {'aband':>5} | {'compl':>5} | "
        f"{'%concl':>6} | {'melhor':>6} | {'média':>6} | {'p50':>4} | {'tempo best (s)':>14}"
    )
    print(header)
    print("-" * len(header))
    for s in store.level_stats():
        print(
            f"{s.level:>4} | {s.total_starts:>6} | {s.total_abandons:>5} | "
            f"{s.total_completions:>5} | {s.completion_rate_pct:>6} | "
            f"{str(s.best_moves):>6} | {str(s.avg_moves):>6} | "
            f"{str(s.moves_p50):>4} | {str(s.best_time_seconds):>14}"
        )
    print()


def main() -> None:
    print_verbose_game()

    store = TelemetryStore("crow_forest_telemetry.db")
    store.log_page_load()

    rng = random.Random(42)
    for level in range(1, 6):
        n_sessions = 30
        for i in range(n_sessions):
            # fases mais avançadas simulam jogadores mais experientes,
            # mas também mais violações simultâneas -> erro base cresce
            # um pouco com a fase, decrescendo com a prática (ruído).
            error_rate = min(0.55, 0.08 + 0.03 * level + rng.uniform(-0.05, 0.05))
            play_one_session(store, level=level, error_rate=error_rate, seed=level * 1000 + i)

    print_stats(store)
    store.close()


if __name__ == "__main__":
    main()
