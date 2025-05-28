from datetime import datetime
import sqlite3

class tugas:
    def __init__(self, judul, deskripsi, deadline, status):
        self.judul = judul
        self.deskripsi = deskripsi
        self.deadline = deadline
        self.status = status

    @staticmethod
    def init_db(dbname="TugasUser.db"):
        conn = sqlite3.connect(dbname)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                judul TEXT NOT NULL,
                deskripsi TEXT NOT NULL,
                deadline TEXT NOT NULL,
                status BOOLEAN DEFAULT 0,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        ''')
        conn.commit()
        conn.close()

    @classmethod
    def simpan(cls,conn, user_id, judul, deskripsi, deadline, status):
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO tasks (user_id, judul, deskripsi, deadline, status)
                VALUES (?, ?, ?, ?, ?)
            """, (user_id, judul, deskripsi, deadline, int(status)))
            conn.commit()
        finally:
            cursor.close()

    @classmethod
    def get_tasks(cls, conn, user_id):
        cursor = conn.cursor()
        cursor.execute("SELECT id, user_id, judul, deskripsi, deadline, status FROM tasks WHERE user_id=?", (user_id,))
        return cursor.fetchall()

    @classmethod
    def edit_task(cls,conn, task_id, judul=None, deskripsi=None, deadline=None, status=None):
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks WHERE id=?", (task_id,))
        task_data = cursor.fetchone()
        if not task_data:
            print(f"Tugas ID {task_id} tidak ditemukan.")
            return False

        new_judul = judul or task_data[2]
        new_deskripsi = deskripsi or task_data[3]
        new_deadline = deadline or task_data[4]
        new_status = status if status is not None else task_data[5]

        cursor.execute("""
            UPDATE tasks SET judul = ?, deskripsi = ?, deadline = ?, status = ?
            WHERE id = ?
        """, (new_judul, new_deskripsi, new_deadline, int(new_status), task_id))
        conn.commit()
        return True

    @classmethod
    def hapus(cls,conn, task_id):
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        conn.commit()
        return cursor.rowcount > 0

    @classmethod
    def tandai_selesai(cls, conn, task_id):
        return cls.edit_task(conn, task_id, status=True)

    @classmethod
    def urutkan_berdasarkan_deadline(cls, user_id, dbname="TugasUser.db"):
        tasks = cls.get_tasks(user_id, dbname)
        try:
            return sorted(tasks, key=lambda x: datetime.strptime(x[4], "%d/%m/%Y %H:%M"))
        except Exception as e:
            print("Error saat sorting:", e)
            return tasks




