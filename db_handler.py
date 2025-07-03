import sqlite3

class DBHandler:
    def __init__(self):
        self.conn = sqlite3.connect("network_log.db", check_same_thread=False)
        self.create_table()

    def create_table(self):
        self.conn.execute('''CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            ip TEXT,
            signal INTEGER,
            status TEXT
        )''')
        self.conn.commit()

    def insert(self, timestamp, ip, signal, status):
        self.conn.execute("INSERT INTO logs (timestamp, ip, signal, status) VALUES (?, ?, ?, ?)",
                          (timestamp, ip, signal, status))
        self.conn.commit()

    def fetch_all(self):
        cursor = self.conn.execute("SELECT timestamp, ip, signal, status FROM logs ORDER BY id DESC LIMIT 100")
        return cursor.fetchall()