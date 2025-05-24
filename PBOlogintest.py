import sqlite3
import hashlib

class Login:
    def __init__(self, Username, Email, Password):
        self.Username = Username
        self.Email = Email
        self.__Password = self.hash_password(Password)
        self.db_name = f"{Email}.db"  # Setiap user punya database sendiri
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        with self.conn:
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Pengguna (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                UserName TEXT NOT NULL,
                Email TEXT UNIQUE NOT NULL,
                Password TEXT NOT NULL
            )
            """)

    # Method untuk hash password
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    # Method Setter
    def set_Username(self):
        self.Username = input("Masukkan Username: ")

    def set_Email(self):
        self.Email = input("Masukkan Email: ")

    def set_Password(self):
        pw = input("Masukkan Password: ")
        self.__Password = self.hash_password(pw)

    # Method Getter
    def get_Username(self):
        return self.Username

    def get_Email(self):
        return self.Email

    def get_Password(self):  # Getter hanya jika benar-benar diperlukan
        return self.__Password

    # Method untuk verifikasi password
    def VerifPassword(self, password):
        return self.__Password == self.hash_password(password)

    # Method Register
    def Register(self):
        self.set_Username()
        self.set_Email()
        self.set_Password()
        
        with self.conn:
            self.cursor.execute("INSERT INTO Pengguna (UserName, Email, Password) VALUES (?, ?, ?)",
                                (self.Username, self.Email, self.__Password))
        print("Registrasi berhasil!")
    
    
    # Method Login
    def Login(self):
        email = input("Masukkan Email: ")
        password = input("Masukkan Password: ")
        
        db_name = f"{email}.db"  # Cek database user tertentu
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        cursor.execute("SELECT Password FROM Pengguna WHERE Email = ?", (email,))
        data = cursor.fetchone()

        if data and data[0] == self.hash_password(password):
            print("Login berhasil!")
        else:
            print("Login gagal. Email atau password salah.")

    # Method Ganti Password
    def GantiPassword(self):
        current_pw = input("Masukkan Password lama: ")
        if self.VerifPassword(current_pw):
            new_pw = input("Masukkan Password baru: ")
            hashed_pw = self.hash_password(new_pw)

            with self.conn:
                self.cursor.execute("UPDATE Pengguna SET Password = ? WHERE Email = ?", (hashed_pw, self.Email))

            print("Password berhasil diubah.")
        else:
            print("Password lama salah.")
