"""
telemetry.py
------------
Pipeline de dados do jogo, na perspectiva de engenharia de dados.

No bundle JS original, o jogo grava eventos numa tabela Supabase
`game_sessions` (funções `Ea`/`Iw`/`Ow`/`Lw`/`Nw`) e consulta uma view
agregada `level_stats` (função `Fw`, chamada por `select('*')`).

Aqui reproduzimos o mesmo contrato de dados localmente com SQLite:
  - `game_sessions`: log de eventos brutos (grão fino, 1 linha por
    evento: start / abandon / complete), igual ao schema original
    (level, moves, time_seconds, nodes_created/actions_created,
    completed, event_type).
  - `level_stats`: view materializada sob demanda, calculada em Python
    (percentis, taxa de conclusão, melhor marca), equivalente à RPC
    `update_world_record` + view `level_stats` do backend original.

Não há dependência externa: só a stdlib (sqlite3), para manter o
pipeline simples de rodar/testar em qualquer ambiente.
"""

from __future__ import annotations

import sqlite3
import statistics
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, List, Dict, Any

DDL = """
CREATE TABLE IF NOT EXISTS game_sessions (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    level           INTEGER,
    moves           INTEGER NOT NULL DEFAULT 0,
    time_seconds    INTEGER NOT NULL DEFAULT 0,
    actions_created INTEGER NOT NULL DEFAULT 0,   -- equivalente a nodes_created no jogo original
    completed       INTEGER NOT NULL DEFAULT 0,   -- 0/1
    event_type      TEXT NOT NULL,                -- page_load | start | abandon | complete
    created_at      TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_sessions_level_event
    ON game_sessions(level, event_type);
"""


@dataclass
class LevelStats:
    level: int
    total_starts: int
    total_abandons: int
    total_completions: int
    completion_rate_pct: float
    best_moves: Optional[int]
    avg_moves: Optional[float]
    avg_moves_on_abandon: Optional[float]
    moves_p25: Optional[int]
    moves_p50: Optional[int]
    moves_p75: Optional[int]
    best_time_seconds: Optional[int]


class TelemetryStore:
    def __init__(self, db_path: str | Path = "crow_forest_telemetry.db") -> None:
        self.db_path = str(db_path)
        self._conn = sqlite3.connect(self.db_path)
        self._conn.executescript(DDL)
        self._conn.commit()

    def close(self) -> None:
        self._conn.close()

    # ------------------------------------------------------------------ #
    # Ingestão de eventos (equivalente a Ea() / Iw() no JS)              #
    # ------------------------------------------------------------------ #
    def log_event(
        self,
        level: Optional[int],
        event_type: str,
        moves: int = 0,
        time_seconds: int = 0,
        actions_created: int = 0,
        completed: bool = False,
    ) -> None:
        self._conn.execute(
            """
            INSERT INTO game_sessions
                (level, moves, time_seconds, actions_created, completed, event_type, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                level,
                moves,
                time_seconds,
                actions_created,
                int(completed),
                event_type,
                datetime.now(timezone.utc).isoformat(),
            ),
        )
        self._conn.commit()

    def log_page_load(self) -> None:
        self.log_event(level=None, event_type="page_load")

    def log_start(self, level: int) -> None:
        self.log_event(level=level, event_type="start")

    def log_abandon(self, level: int, moves: int, time_seconds: int, actions_created: int) -> None:
        self.log_event(
            level=level,
            event_type="abandon",
            moves=moves,
            time_seconds=time_seconds,
            actions_created=actions_created,
        )

    def log_complete(self, level: int, moves: int, time_seconds: int, actions_created: int) -> Dict[str, Any]:
        self.log_event(
            level=level,
            event_type="complete",
            moves=moves,
            time_seconds=time_seconds,
            actions_created=actions_created,
            completed=True,
        )
        return self._update_personal_best(level, moves)

    # ------------------------------------------------------------------ #
    # "Recorde pessoal" local (equivalente ao localStorage do jogo       #
    # original + RPC update_world_record)                                #
    # ------------------------------------------------------------------ #
    def _update_personal_best(self, level: int, moves: int) -> Dict[str, Any]:
        row = self._conn.execute(
            """
            SELECT MIN(moves) FROM game_sessions
            WHERE level = ? AND event_type = 'complete' AND moves < ?
            """,
            (level, moves),
        ).fetchone()
        is_new_best = row[0] is None
        return {"level": level, "moves": moves, "is_new_best": is_new_best}

    # ------------------------------------------------------------------ #
    # Agregação analítica (equivalente à view level_stats / função Fw)   #
    # ------------------------------------------------------------------ #
    def level_stats(self) -> List[LevelStats]:
        levels = [
            r[0]
            for r in self._conn.execute(
                "SELECT DISTINCT level FROM game_sessions WHERE level IS NOT NULL ORDER BY level"
            ).fetchall()
        ]
        results: List[LevelStats] = []
        for level in levels:
            starts = self._count(level, "start")
            abandons = self._count(level, "abandon")
            completions = self._count(level, "complete")
            completion_rate = round(100 * completions / starts, 1) if starts else 0.0

            completed_moves = self._moves(level, "complete")
            abandon_moves = self._moves(level, "abandon")
            best_time = self._best_time(level)

            results.append(
                LevelStats(
                    level=level,
                    total_starts=starts,
                    total_abandons=abandons,
                    total_completions=completions,
                    completion_rate_pct=completion_rate,
                    best_moves=min(completed_moves) if completed_moves else None,
                    avg_moves=round(statistics.mean(completed_moves), 1) if completed_moves else None,
                    avg_moves_on_abandon=round(statistics.mean(abandon_moves), 1) if abandon_moves else None,
                    moves_p25=self._percentile(completed_moves, 25),
                    moves_p50=self._percentile(completed_moves, 50),
                    moves_p75=self._percentile(completed_moves, 75),
                    best_time_seconds=best_time,
                )
            )
        return results

    # -- helpers ---------------------------------------------------------
    def _count(self, level: int, event_type: str) -> int:
        return self._conn.execute(
            "SELECT COUNT(*) FROM game_sessions WHERE level = ? AND event_type = ?",
            (level, event_type),
        ).fetchone()[0]

    def _moves(self, level: int, event_type: str) -> List[int]:
        return [
            r[0]
            for r in self._conn.execute(
                "SELECT moves FROM game_sessions WHERE level = ? AND event_type = ?",
                (level, event_type),
            ).fetchall()
        ]

    def _best_time(self, level: int) -> Optional[int]:
        row = self._conn.execute(
            "SELECT MIN(time_seconds) FROM game_sessions WHERE level = ? AND event_type = 'complete'",
            (level,),
        ).fetchone()
        return row[0]

    @staticmethod
    def _percentile(values: List[int], pct: int) -> Optional[int]:
        if not values:
            return None
        s = sorted(values)
        k = (len(s) - 1) * (pct / 100)
        f, c = int(k), min(int(k) + 1, len(s) - 1)
        if f == c:
            return s[f]
        return round(s[f] + (s[c] - s[f]) * (k - f))
