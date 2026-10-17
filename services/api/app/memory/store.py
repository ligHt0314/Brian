import json
import sqlite3
import threading
from pathlib import Path
from app.domain.models import now_iso


class Store:
    def __init__(self, path: str):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        self.lock = threading.RLock()
        self.db = sqlite3.connect(path, check_same_thread=False)
        self.db.execute("PRAGMA journal_mode=WAL")
        self.db.execute("PRAGMA foreign_keys=ON")
        self.db.execute(
            "CREATE TABLE IF NOT EXISTS records (id TEXT PRIMARY KEY, kind TEXT, actor TEXT, data TEXT, created_at TEXT)"
        )
        self.db.commit()

    def put(self, id: str, kind: str, actor: str, data: dict):
        with self.lock, self.db:
            self.db.execute(
                "INSERT INTO records VALUES (?,?,?,?,?) ON CONFLICT(id) DO UPDATE SET data=excluded.data",
                (id, kind, actor, json.dumps(data), now_iso()),
            )

    def get(self, id: str, kind: str, actor: str | None = None) -> dict | None:
        with self.lock:
            row = self.db.execute(
                "SELECT actor,data FROM records WHERE id=? AND kind=?", (id, kind)
            ).fetchone()
            if row and (actor is None or row[0] == actor):
                return json.loads(row[1])
        return None

    def list(self, kind: str, actor: str | None = None) -> list[dict]:
        with self.lock:
            rows = self.db.execute(
                "SELECT actor,data FROM records WHERE kind=? ORDER BY created_at DESC", (kind,)
            ).fetchall()
            return [json.loads(r[1]) for r in rows if actor is None or r[0] == actor]
