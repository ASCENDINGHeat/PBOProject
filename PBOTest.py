from datetime import datetime
import sqlite3

# class tugas:
#     def __init__ (self, judul, deskripsi, deadline, status):
#         self.judul = judul
#         self.deskripsi = deskripsi
#         self.deadline = deadline
#         self.status = status
        

#     def close(self):
#         if self.conn:
#             self.conn.close()
#             self.conn = None

#     def __del__(self):
#         self.close()
    
#     # Method Setter
#     def set_Judul(self, judul):
#         self.judul = judul

#     def set_Deskripsi(self, deskripsi):
#         self.deskripsi = deskripsi

#     def set_Deadline(self, deadline):
#         self.deadline = deadline

#     def set_Status(self, status):
#         self.status = status

#     # Method Getter
#     def get_Judul(self):
#         return self.judul
    
#     def get_Deskripsi(self):
#         return self.deskripsi 
    
#     def get_Deadline(self):
#         return self.deadline
    
#     def get_Status(self):
#         return self.status


#     method
#     def add_task(self, user_id, judul, deskripsi, deadline, status):
#         cursor = self.conn.cursor()
#         try:
#             cursor.execute("INSERT INTO tasks (user_id,judul,deskripsi,deadline,status ) VALUES (?, ?, ?, ?, ?)", (user_id, judul, deskripsi, deadline, status))
#             self.conn.commit()
#         finally:
#             cursor.close()
#             self.conn.close()
            
#     def get_tasks(self, user_id):
#         # conn = sqlite3.connect("TugasUser.db")
#         cursor = self.conn.cursor()
#         cursor.execute("SELECT * FROM tasks WHERE user_id=?", (user_id,))
#         return cursor.fetchall()
    
#     def edit_task(self, task_id, judul=None, deskripsi=None, deadline=None):
#         cursor = self.conn.cursor()

#         # Ambil data lama
#         cursor.execute("SELECT * FROM tasks WHERE id=?", (task_id,))
#         task_data = cursor.fetchone()
#         if not task_data:
#             print(f"Tugas dengan ID {task_id} tidak ditemukan.")
#             return False

#         # Jika field tidak diisi, gunakan nilai lama
#         judul = judul if judul is not None else task_data[2]
#         deskripsi = deskripsi if deskripsi is not None else task_data[3]
#         deadline = deadline if deadline is not None else task_data[4]
#         status = status if status is not None else task_data[5]

#         # Update ke database
#         cursor.execute("""
#             UPDATE tasks
#             SET judul = ?, deskripsi = ?, deadline = ?, status = ?
#             WHERE id = ?
#         """, (judul, deskripsi, deadline, status, task_id))

#         self.conn.commit()
#         print(f"Tugas ID {task_id} berhasil diperbarui.")
#         return True
    
#     def delete_task(self, task_id):
#         cursor = self.conn.cursor()
#         cursor.execute("SELECT * FROM tasks WHERE id=?", (task_id,))
#         if not cursor.fetchone():
#             print(f"Tugas dengan ID {task_id} tidak ditemukan.")
#             return False

#         cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))
#         self.conn.commit()
#         print(f"Tugas ID {task_id} berhasil dihapus.")
#         return True
#     def TambahTugas(self):
#         input_judul = input(self.judul)
#         input_deskripsi = input(self.deskripsi)
#         input_deadline = datetime.strptime(input(self.deadline), '%d-%m-%Y %H:%M')
#         input_status = False
        
#         tugas_baru = tugas(input_judul, input_deskripsi, input_deadline, input_status)    
        
#     def EditTugas(self):
#         with open('tugas.txt', 'r') as f:
#             lines = f.readlines()
        
#         with open('tugas.txt', 'w') as f: 
#             for line in lines:
#                 if line.startswith(self.judul):
#                     line = f"{self.judul}, {self.deskripsi}, {self.deadline}\n"
#                 f.write(line)

#     def tandaiSelesai(self, tugas_list, filename =""):
#         self.status = True
        
#     def HapusTugas(self, task_id):
#         cursor = self.conn.cursor()
#         cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
#         self.conn.commit()
#         self.conn.close()
   
#     def load_tugas(filename="tugas_data.txt"):
#         tugas_list = []
#         try:
#             with open(filename, "r", encoding="utf-8") as f:
#                 lines = f.read().split("--------------------------\n")
#                 for entry in lines:
#                     if entry.strip():
#                         parts = entry.strip().split("\n")
#                         if len(parts) >= 4:
#                             judul = parts[0]
#                             deskripsi = parts[1]
#                             deadline = parts[2]
#                             status = parts[3] == "True"
#                             tugas_obj = tugas(judul, deskripsi, deadline, status)
#                             tugas_list.append(tugas_obj)
#         except FileNotFoundError:
#             pass
#         return tugas_list

#     def save_all_tugas(tugas_list, filename="tugas_data.txt"):
#         with open(filename, "w", encoding="utf-8") as f:
#             for tugas_obj in tugas_list:
#                 f.write(f"{tugas_obj.judul}\n{tugas_obj.deskripsi}\n{tugas_obj.deadline}\n{tugas_obj.status}\n--------------------------\n")

#     def add_tugas(tugas_obj, filename="tugas_data.txt"):
#         with open(filename, "a", encoding="utf-8") as f:
#             f.write(f"{tugas_obj.judul}\n{tugas_obj.deskripsi}\n{tugas_obj.deadline}\n{tugas_obj.status}\n--------------------------\n")

#     def sorting_tugas_deadline(tugas_list):
#         return sorted(
#             tugas_list, key=lambda t: datetime.strptime(str(t.deadline), '%d/%m/%Y %H:%M') if isinstance(t.deadline, str) else t.deadline
#         )
    
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



class User:
    def __init__(self, id, username):
        self.id = id
        self.username = username

class AuthSystem:
    def __init__(self, conn):
        self.conn = conn

    def register(self, username, email, password):
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO users (username, email, password)
                VALUES (?, ?, ?)
            """, (username, email, password))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError as e:
            self.conn.rollback()
            return False, str(e)

    def login(self, identifier, password):
        cursor = self.conn.cursor()
        query = """
            SELECT id, username FROM users 
            WHERE (username = ? OR email = ?) AND password = ?
        """
        cursor.execute(query, (identifier, identifier, password))
        user_data =  cursor.fetchone()
        if user_data:
            return User(user_data[0], user_data[1])
        return None
# class TaskManager:
#     def __init__(self, db_name="TugasUser.db"):
#         self.conn = sqlite3.connect(db_name)

#     def add_task(self, user_id, task):
#         cursor = self.conn.cursor()
#         cursor.execute("INSERT INTO tasks (user_id, task) VALUES (?, ?)", (user_id, task))
#         self.conn.commit()

#     def get_tasks(self, user_id):
#         cursor = self.conn.cursor()
#         cursor.execute("SELECT id, task, completed FROM tasks WHERE user_id = ?", (user_id,))
#         return cursor.fetchall()

#     def mark_complete(self, task_id):
#         cursor = self.conn.cursor()
#         cursor.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (task_id,))
        # self.conn.commit()

# Inisialisasi
#auth = AuthSystem()
#tugas_ = tugas( "Belajar Python", "Pelajari dasar-dasar Python", "2023/12/31 23:59", 0)

# Registrasi
# auth.register("alice", "alice@email.com", "password123")
# auth.register("bob", "bob@email.com", "password456")
# auth.register("charlie", "charlie@email.com", "password789")
#auth.register("dika", "dika@gmail.com", "dika123")

# Login
# user = auth.login("alice", "password123")
# user2 = auth.login("bob", "password456")
# user3 = auth.login("charlie", "password789")
# user = auth.login("dika", "dika123")
# if user:
#     tugas_.add_task(user.id, "Belajar Python", "Pelajari dasar-dasar Python", "2023/12/31 23:59", 0)
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

# if user3:
#     Menambahkan tugas untuk user3
#     task_manager.add_task(user3.id, "Belajar Web Development")
#     task_manager.add_task(user3.id, "Tugas Matematika Diskrit")

#     Mendapatkan tugas untuk user3
#     tasks3 = task_manager.get_tasks(user3.id)
#     for task in tasks3:
#         print(task)




