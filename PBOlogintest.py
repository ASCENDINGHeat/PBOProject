import hashlib
class Login:
    def __init__(self, Username, Email, Password):
        self.Username = Username
        self.Email = Email
        self.__Password = self.hash_password(Password)

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
        print("Registrasi berhasil!")

    # Method Login
    def Login(self):
        username = input("Masukkan Username: ")
        password = input("Masukkan Password: ")

        if username == self.Username and self.VerifPassword(password):
            print("Login berhasil!")
        else:
            print("Login gagal. Username atau password salah.")

    # Method Ganti Password
    def GantiPassword(self):
        current_pw = input("Masukkan Password lama: ")
        if self.VerifPassword(current_pw):
            new_pw = input("Masukkan Password baru: ")
            self.__Password = self.hash_password(new_pw)
            print("Password berhasil diubah.")
        else:
            print("Password lama salah.")
