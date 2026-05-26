"""
db.py - SQLite storage layer for helpdesk ticket tracker
"""

import sqlite3
from datetime import datetime

DB_PATH = "tickets.db"

class TicketDB:
    def __init__(self, path=DB_PATH):
        self.conn = sqlite3.connect(path)
        self.conn.row_factory = sqlite3.Row
        self._init_schema()

    def _init_schema(self):
        self.conn.executescript("""
            CREATE TABLE IF NOT EXISTS tickets (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                title       TEXT NOT NULL,
                status      TEXT NOT NULL DEFAULT 'open',
                priority    TEXT NOT NULL DEFAULT 'medium',
                created_at  TEXT NOT NULL,
                updated_at  TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS notes (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                ticket_id   INTEGER NOT NULL REFERENCES tickets(id),
                note        TEXT NOT NULL,
                created_at  TEXT NOT NULL
            );
        """)
        self.conn.commit()

    def _now(self):
        return datetime.now().isoformat(sep=" ", timespec="seconds")

    def create_ticket(self, title, priority="medium"):
        now = self._now()
        cur = self.conn.execute(
            "INSERT INTO tickets (title, priority, created_at, updated_at) VALUES (?, ?, ?, ?)",
            (title, priority, now, now)
        )
        self.conn.commit()
        return cur.lastrowid

    def list_tickets(self, status=None):
        if status:
            rows = self.conn.execute(
                "SELECT * FROM tickets WHERE status = ? ORDER BY id DESC", (status,)
            ).fetchall()
        else:
            rows = self.conn.execute(
                "SELECT * FROM tickets ORDER BY id DESC"
            ).fetchall()
        return [dict(r) for r in rows]

    def get_ticket(self, ticket_id):
        row = self.conn.execute(
            "SELECT * FROM tickets WHERE id = ?", (ticket_id,)
        ).fetchone()
        return dict(row) if row else None

    def update_ticket(self, ticket_id, status=None, note=None):
        now = self._now()
        if status:
            self.conn.execute(
                "UPDATE tickets SET status = ?, updated_at = ? WHERE id = ?",
                (status, now, ticket_id)
            )
        if note:
            self.conn.execute(
                "INSERT INTO notes (ticket_id, note, created_at) VALUES (?, ?, ?)",
                (ticket_id, note, now)
            )
        self.conn.commit()

    def get_notes(self, ticket_id):
        rows = self.conn.execute(
            "SELECT * FROM notes WHERE ticket_id = ? ORDER BY id", (ticket_id,)
        ).fetchall()
        return [dict(r) for r in rows]
