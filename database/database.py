import os
import sqlite3
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(DATABASE_DIR, "penales.db")


class GameDatabase:
    def __init__(self, player_name="Jugador"):
        os.makedirs(DATABASE_DIR, exist_ok=True)
        self.player_name = player_name
        self.connection = sqlite3.connect(DATABASE_PATH)
        self.connection.row_factory = sqlite3.Row
        self._create_tables()
        self._ensure_player()

    def _create_tables(self):
        with self.connection:
            self.connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS players (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    points INTEGER NOT NULL DEFAULT 0,
                    goals INTEGER NOT NULL DEFAULT 0,
                    shots INTEGER NOT NULL DEFAULT 0,
                    completed_levels INTEGER NOT NULL DEFAULT 0,
                    updated_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS achievements (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    player_id INTEGER NOT NULL,
                    level INTEGER NOT NULL,
                    title TEXT NOT NULL,
                    earned_at TEXT NOT NULL,
                    UNIQUE(player_id, level),
                    FOREIGN KEY(player_id) REFERENCES players(id)
                );
                """
            )

    def _ensure_player(self):
        now = datetime.now().isoformat(timespec="seconds")
        with self.connection:
            self.connection.execute(
                "INSERT OR IGNORE INTO players (name, updated_at) VALUES (?, ?)",
                (self.player_name, now),
            )
        row = self.connection.execute(
            "SELECT id FROM players WHERE name = ?", (self.player_name,)
        ).fetchone()
        self.player_id = row["id"]

    def register_shot(self, scored=False, level=1):
        points = (100 + level * 25) if scored else 0
        now = datetime.now().isoformat(timespec="seconds")
        with self.connection:
            self.connection.execute(
                """
                UPDATE players
                SET points = points + ?, goals = goals + ?, shots = shots + 1,
                    updated_at = ?
                WHERE id = ?
                """,
                (points, int(scored), now, self.player_id),
            )

    def register_achievement(self, level):
        now = datetime.now().isoformat(timespec="seconds")
        with self.connection:
            result = self.connection.execute(
                """
                INSERT OR IGNORE INTO achievements (player_id, level, title, earned_at)
                VALUES (?, ?, ?, ?)
                """,
                (self.player_id, level, f"Medalla nivel {level}", now),
            )
            if result.rowcount:
                self.connection.execute(
                    "UPDATE players SET completed_levels = completed_levels + 1, updated_at = ? WHERE id = ?",
                    (now, self.player_id),
                )

    def get_player_stats(self):
        return self.connection.execute(
            "SELECT points, goals, shots, completed_levels FROM players WHERE id = ?",
            (self.player_id,),
        ).fetchone()

    def get_ranking(self, limit=5):
        return self.connection.execute(
            """
            SELECT name, points, goals, completed_levels
            FROM players
            ORDER BY points DESC, goals DESC, completed_levels DESC, name ASC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

    def close(self):
        self.connection.close()
