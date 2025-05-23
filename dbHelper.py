import sqlite3

class DBHelper:
    def __init__(self, db_name="tugas.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS tugas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    judul TEXT,
                    deskripsi TEXT,
                    deadline TEXT,
                    status INTEGER
                )
            """)

    def add_tugas(self, judul, deskripsi, deadline, status):
        with self.conn:
            self.conn.execute(
                "INSERT INTO tugas (judul, deskripsi, deadline, status) VALUES (?, ?, ?, ?)",
                (judul, deskripsi, deadline, int(status))
            )

    def get_all_tugas(self):
        with self.conn:
            return self.conn.execute("SELECT id, judul, deskripsi, deadline, status FROM tugas").fetchall()

    def update_tugas(self, id, judul, deskripsi, deadline, status):
        with self.conn:
            self.conn.execute(
                "UPDATE tugas SET judul=?, deskripsi=?, deadline=?, status=? WHERE id=?",
                (judul, deskripsi, deadline, int(status), id)
            )

    def delete_tugas(self, id):
        with self.conn:
            self.conn.execute("DELETE FROM tugas WHERE id=?", (id,))