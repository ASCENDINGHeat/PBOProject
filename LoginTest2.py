import sqlite3

def init_db():
    conn = sqlite3.connect("TugasUser.db")
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
            task TEXT NOT NULL,
            completed BOOLEAN NOT NULL DEFAULT 0,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')
    conn.commit()
    conn.close()
init_db()
class User:
    def __init__(self, id, username):
        self.id = id
        self.username = username

class AuthSystem:
    def __init__(self):
        self.conn = sqlite3.connect("TugasUser.db")

    def register(self, username, email, password):
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO users (username, email, password) 
                VALUES (?, ?, ?)
            """, (username, email, password))
            self.conn.commit()
            print("Registrasi berhasil!")
            return True
        except sqlite3.IntegrityError as e:
            if "UNIQUE constraint failed: users.username" in str(e):
                print("Username sudah terdaftar.")
            elif "UNIQUE constraint failed: users.email" in str(e):
                print("Email sudah terdaftar.")
            else:
                print("Error:", e)
            return False
    def login(self, identifier, password):
        """
        identifier bisa berupa username atau email
        """
        cursor = self.conn.cursor()
        query = """
            SELECT id, username FROM users 
            WHERE (username = ? OR email = ?) AND password = ?
        """
        cursor.execute(query, (identifier, identifier, password))
        user_data = cursor.fetchone()
        if user_data:
            print("Login berhasil!")
            return User(id=user_data[0], username=user_data[1])
        else:
            print("Login gagal. Username/email atau password salah.")
            return None
class TaskManager:
    def __init__(self, db_name="TugasUser.db"):
        self.conn = sqlite3.connect(db_name)

    def add_task(self, user_id, task):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO tasks (user_id, task) VALUES (?, ?)", (user_id, task))
        self.conn.commit()

    def get_tasks(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, task, completed FROM tasks WHERE user_id = ?", (user_id,))
        return cursor.fetchall()

    def mark_complete(self, task_id):
        cursor = self.conn.cursor()
        cursor.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (task_id,))
        self.conn.commit()

# Inisialisasi
auth = AuthSystem()
task_manager = TaskManager()

# Registrasi
# auth.register("alice", "alice@email.com", "password123")
# auth.register("bob", "bob@email.com", "password456")
# auth.register("charlie", "charlie@email.com", "password789")

# Login
# user = auth.login("alice", "password123")
# user2 = auth.login("bob", "password456")
user3 = auth.login("charlie", "password789")

# if user:
    # Menambahkan tugas
    # task_manager.add_task(user.id, "Belajar Python")
    # task_manager.add_task(user.id, "Tugas Projek PBO")

    # Mendapatkan tugas
    # tasks = task_manager.get_tasks(user.id)
    # for task in tasks:
    #     print(task)

    # Menandai tugas selesai
    # task_manager.mark_complete(1)

# if user2:
#     # Menambahkan tugas untuk user2
#     task_manager.add_task(user2.id, "Belajar SQL")
#     task_manager.add_task(user2.id, "Tugas Database")

#     # Mendapatkan tugas untuk user2
#     tasks2 = task_manager.get_tasks(user2.id)
#     for task_id, task_text, completed in tasks2:
#         status = "Selesai" if completed else "Belum Selesai"
#         print(f"{task_id}. {task_text} - {status}")

if user3:
    # Menambahkan tugas untuk user3
    # task_manager.add_task(user3.id, "Belajar Web Development")
    # task_manager.add_task(user3.id, "Tugas Matematika Diskrit")

    # Mendapatkan tugas untuk user3
    tasks3 = task_manager.get_tasks(user3.id)
    for task in tasks3:
        print(task)