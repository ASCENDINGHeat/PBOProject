from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem
from PyQt6.QtCore import QDateTime
import sqlite3
from PBOTest import *
from qt_material import apply_stylesheet

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("UItest.ui", self)
        self.conn = sqlite3.connect("TugasUser.db")
        self.stackedWidget.setCurrentIndex(0)
        self.pushButtonLOGIN.clicked.connect(lambda :self.loginPage())
        self.pushButtonFILL.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))

        self.pushButtonSubmit.clicked.connect(self.fillAtrribute)
        self.pushButtonView.clicked.connect(self.viewSelectedTugas)
        self.pushButtonBack.clicked.connect(lambda: (self.stackedWidget.setCurrentIndex(1), self.viewAttribute()))
        self.pushButtonBack_2.clicked.connect(lambda: (self.stackedWidget.setCurrentIndex(1), self.viewAttribute()))

        self.pushButtonEdit.clicked.connect(self.editTugas) 
        self.pushButtonSave.clicked.connect(self.saveEditedTugas)
        self.pushButtonDelete.clicked.connect(self.deleteTugas)
        self.pushButtonSORT.clicked.connect(self.sortTugas)
        self.pushButtonDone.clicked.connect(self.TandaiSelesai)
        self.pushButtonRegist.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(5))
        self.pushButtonBackRegist.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))

        self.tugas_list = []
        self.selected_row = None
        self.tugas_manager = tugas("", "", "", 0)  # Inisialisasi tugas_manager tanpa data awal

    def sortTugas(self):
        self.tugas_list = tugas.sorting_tugas_deadline(self.tugas_list)
        tugas.save_all_tugas(self.tugas_list)
        self.viewAttribute()
        
    def TandaiSelesai(self):
        selected_row = self.tableWidget.currentRow()
        if selected_row >=0 and self.tugas_list[selected_row].status == False:
            t = self.tugas_list[selected_row]
            t.status = True
            tugas.save_all_tugas(self.tugas_list)
            QMessageBox.information(self, "Success", f"Tugas '{t.judul}' telah ditandai selesai!")
            self.viewAttribute()
        else:
            if self.tugas_list[selected_row].status == True:
                QMessageBox.warning(self, "Tugas Sudah Selesai", "Tugas ini sudah ditandai selesai.")
            else:
                QMessageBox.warning(self, "Pilih Tugas", "Silahkan pilih tugas terlebih dahulu.")

    def fillAtrribute(self, user_id):
        judul = self.lineEditName.text()
        deskripsi = self.lineEditDesc.text()
        deadline = self.dateTimeEdit.dateTime().toString('dd/MM/yyyy HH:mm')
        status = False
        tugas_obj = tugas(judul, deskripsi, deadline, status)
        self.tugas_list.append(tugas_obj)
        self.tugas_manager.add_task(self.user_id, judul, deskripsi, deadline, status)  
        
        QMessageBox.information(self, "Success", f"Tugas '{tugas_obj.judul}' added successfully!")
        self.stackedWidget.setCurrentIndex(1)
        self.viewAttribute()

    def viewAttribute(self):
    # Ambil data tugas dari database untuk user yang sedang login
        if not hasattr(self, 'user_id'):
            QMessageBox.warning(self, "Error", "User belum login.")
            return

        tasks = self.tugas_manager.get_tasks(self.user_id)
        
        self.tableWidget.setRowCount(len(tasks))
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(["Judul", "Deadline", "Status"])
        for row, task in enumerate(tasks):
            # task: (id, judul, deskripsi, deadline, status)
            # Pastikan urutan kolom sesuai dengan SELECT di get_tasks
            judul = task[2]
            deadline = task[4]
            status = "Selesai" if task[5] else "Belum Selesai"
            self.tableWidget.setItem(row, 0, QTableWidgetItem(judul))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(deadline))
            self.tableWidget.setItem(row, 2, QTableWidgetItem(status))
            
    def viewSelectedTugas(self):
        self.stackedWidget.setCurrentIndex(3)
        selected_row = self.tableWidget.currentRow()
        if selected_row >= 0:
            t = self.tugas_list[selected_row]
            details = (
            f"Judul      : {t.judul}\n"
            f"Deskripsi  : {t.deskripsi}\n"
            f"Deadline   : {t.deadline}\n"
            f"Status     : {'Selesai' if t.status else 'Belum Selesai'}"
            )
            self.textBrowserDetails.setText(details)
        else:
            QMessageBox.warning(self, "Pilih Tugas", "Silahkan pilih tugas terlebih dahulu.")

    def editTugas(self):
        self.stackedWidget.setCurrentIndex(4)
        selected_row = self.tableWidget.currentRow()
        if selected_row >= 0:
            self.selected_row = selected_row
            self.lineEdit.setText(self.tableWidget.item(selected_row, 0).text())
            self.lineEdit_2.setText(self.tableWidget.item(selected_row, 1).text())
            deadline_str = self.tableWidget.item(selected_row, 2).text()
            dt = QDateTime.fromString(deadline_str, 'dd/MM/yyyy HH:mm')
            self.dateTimeEdit_2.setDateTime(dt)

    def saveEditedTugas(self):
        if self.selected_row is not None:
            t = self.tugas_list[self.selected_row]
            t.judul = self.lineEdit.text()
            t.deskripsi = self.lineEdit_2.text()
            t.deadline = self.dateTimeEdit_2.dateTime().toString('dd/MM/yyyy HH:mm')
            tugas.save_all_tugas(self.tugas_list)
            QMessageBox.information(self, "Success", "Tugas berhasil diubah!")
            self.stackedWidget.setCurrentIndex(1)
            self.selected_row = None
            self.viewAttribute()

    def deleteTugas(self):
        selected_row = self.tableWidget.currentRow()
        if selected_row >= 0:
            response = QMessageBox.question(self, "Delete", "Apakah Anda yakin ingin menghapus tugas ini?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if response == QMessageBox.StandardButton.Yes:
                del self.tugas_list[selected_row]
                self.tableWidget.removeRow(selected_row)
                tugas.save_all_tugas(self.tugas_list)
                QMessageBox.information(self, "Success", "Tugas berhasil dihapus!")
                self.viewAttribute()

    def loginPage(self):
        username = self.lineEditUsername.text()
        password = self.lineEditPassword.text()
        user = auth.login(username, password)  # auth is your AuthSystem instance

        if user:
            self.user_id = user.id  # Store user id for session
            self.stackedWidget.setCurrentIndex(1)
            self.viewAttribute()  # Load user-specific tasks
            QMessageBox.information(self, "Login Berhasil", f"Selamat datang, {user.username}!")
        else:
            QMessageBox.warning(self, "Login Gagal", "Username/email atau password salah.")
        
    def registerUser(self):
        username = self.lineEditUsernameRegist.text()
        email = self.lineEditEmailRegist.text()
        password = self.lineEditPasswordRegist.text()

        if not username or not email or not password:
            QMessageBox.warning(self, "Error", "Semua field harus diisi.")
            return

        if auth.register(username, email, password):
            QMessageBox.information(self, "Success", "Registrasi berhasil!")
            self.stackedWidget.setCurrentIndex(0)
        else:
            QMessageBox.warning(self, "Error", "Registrasi gagal. Mungkin email sudah terdaftar.")
        

app = QApplication([])
apply_stylesheet(app, theme='dark_blue.xml')
window = MyWindow()
window.show()
app.exec()