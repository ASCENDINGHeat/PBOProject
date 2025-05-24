import sqlite3
import hashlib

class DBHelper:
    def __init__(self, email):
        self.db_name = f"{email}.db"  # Setiap pengguna punya database sendiri
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        with self.conn:
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Tugas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                judulTugas TEXT NOT NULL,
                deskripsiTugas TEXT NOT NULL,
                deadLine TEXT NOT NULL,
                selesai BOOLEAN DEFAULT 0
            )
            """)

    def tambah_tugas(self, judul, deskripsi, deadline):
        with self.conn:
            self.cursor.execute(
            "INSERT INTO Tugas (judulTugas, deskripsiTugas, deadLine) VALUES (?, ?, ?)",
            (judul, deskripsi, deadline)
        )
        
        
    def edit_tugas(self, tugas_id, deskripsi_baru, deadline_baru):
        with self.conn:
            self.cursor.execute(
            "UPDATE Tugas SET deskripsiTugas = ?, deadLine = ? WHERE id = ?",
            (deskripsi_baru, deadline_baru, tugas_id)
        )
        

    def lihat_semua_tugas(self):
        with self.conn:
            return self.cursor.execute("SELECT id, judulTugas, deskripsiTugas, deadLine, selesai FROM Tugas").fetchall()
        
        

    def update_tugas(self, id, judul, deskripsi, deadline, status):
        with self.conn:
            self.conn.execute(
                "UPDATE tugas SET judul=?, deskripsi=?, deadline=?, status=? WHERE id=?",
                (judul, deskripsi, deadline, int(status), id)
            )
            

    def hapus_tugas(self, tugas_id):
        with self.conn:
            self.cursor.execute("DELETE FROM Tugas WHERE id = ?", (tugas_id,))

