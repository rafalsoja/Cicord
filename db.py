# cogs/verify_db.py
import sqlite3
from typing import Optional, Tuple

DB_PATH = "verify.sqlite3"

class VerificationDB:
    def __init__(self, path: str = DB_PATH):
        self.conn = sqlite3.connect(path)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS verification (
                guild_id   INTEGER PRIMARY KEY,
                channel_id INTEGER NOT NULL,
                message_id INTEGER NOT NULL,
                role_id    INTEGER NOT NULL,
                secret     TEXT    NOT NULL,
                question   TEXT    NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.conn.commit()

    def upsert_guild(self, guild_id, channel_id, message_id, role_id, secret, question):
        self.conn.execute("""
            INSERT INTO verification (guild_id, channel_id, message_id, role_id, secret, question)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(guild_id) DO UPDATE SET
                channel_id=excluded.channel_id,
                message_id=excluded.message_id,
                role_id=excluded.role_id,
                secret=excluded.secret,
                question=excluded.question
        """, (guild_id, channel_id, message_id, role_id, secret, question))
        self.conn.commit()

    def get_guild(self, guild_id) -> Optional[Tuple[int, int, int, int, str, str]]:
        cur = self.conn.execute("""
            SELECT guild_id, channel_id, message_id, role_id, secret, question
            FROM verification WHERE guild_id=?
        """, (guild_id,))
        return cur.fetchone()

    def delete_guild(self, guild_id):
        self.conn.execute("DELETE FROM verification WHERE guild_id=?", (guild_id,))
        self.conn.commit()

    def all_guilds(self):
        cur = self.conn.execute("""
            SELECT guild_id, channel_id, message_id, role_id, secret, question
            FROM verification
        """)
        return cur.fetchall()
    async def setup(self):
        print("✅ DB loaded successfully.")