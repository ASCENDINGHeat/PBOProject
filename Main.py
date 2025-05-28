from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem, QHeaderView
from PyQt6.QtCore import QDateTime
from PyQt6.QtCore import Qt
import sqlite3
from Logic import tugas
from LoginLogic import User, AuthSystem
from datetime import datetime
from qt_material import apply_stylesheet
import sys
import os

if getattr(sys, 'frozen', False):
    # Running in a bundle
    base_path = sys._MEIPASS
else:
    # Running in normal Python
    base_path = os.path.dirname(__file__)

ui_path = os.path.join(base_path, "UItest.ui")

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("UItest.ui", self)
        
        self.stackedWidget.setCurrentIndex(0)
        self.pushButtonLOGIN.clicked.connect(lambda :self.loginPage())
        self.pushButtonFILL.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))
        self.dateTimeEdit.setDateTime(QDateTime.currentDateTime())

        self.pushButtonSubmit.clicked.connect(self.fillAtrribute)
        self.pushButtonBackDetail.clicked.connect(lambda: (self.stackedWidget.setCurrentIndex(1), self.viewAttribute()))
        self.pushButtonBack_2.clicked.connect(lambda: (self.stackedWidget.setCurrentIndex(1), self.viewAttribute()))

        self.pushButtonEdit.clicked.connect(self.editTugas) 
        self.pushButtonSave.clicked.connect(self.saveEditedTugas)
        self.pushButtonDelete.clicked.connect(self.deleteTugas)
        self.pushButtonDone.clicked.connect(self.TandaiSelesai)
        self.pushButtonRegist.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(5))
        self.pushButtonRegisterPage.clicked.connect(self.registerUser)
        self.pushButtonBackRegist.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.tableWidget.itemSelectionChanged.connect(self.viewSelectedTugas)

        self.tugas_list = []
        self.selected_row = None
        self.conn = sqlite3.connect("TugasUser.db",check_same_thread=False)
        self.auth = AuthSystem(self.conn)
        self.user_id = None
        try:
            tugas.init_db("TugasUser.db")
        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Gagal membuat/mengakses database: {e}")
            sys.exit(1)        

        # Set table header resize mode
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    def sortTugas(self):
        if not hasattr(self, 'user_id'):
            QMessageBox.warning(self, "Error", "Login dulu untuk melihat tugas.")
            return

        sorted_tasks = tugas.urutkan_berdasarkan_deadline(self.user_id)
        self.tableWidget.setRowCount(len(sorted_tasks))

        for row, task in enumerate(sorted_tasks):
            judul_item = QTableWidgetItem(task[2])
            judul_item.setData(Qt.ItemDataRole.UserRole, task[0])

            self.tableWidget.setItem(row, 0, judul_item)
            self.tableWidget.setItem(row, 1, QTableWidgetItem(task[4]))
            self.tableWidget.setItem(row, 2, QTableWidgetItem("Selesai" if task[5] else "Belum Selesai"))

        QMessageBox.information(self, "Sukses", "Tugas diurutkan berdasarkan deadline.")
        
    def TandaiSelesai(self):
        selected_indexes = self.tableWidget.selectionModel().selectedRows()
        
        # if not selected_indexes:
        #     QMessageBox.warning(self, "Pilih Tugas", "Silakan pilih tugas terlebih dahulu.")
        #     return

        selected_row = selected_indexes[0].row()
        judul_item = self.tableWidget.item(selected_row, 0)

        if not judul_item:
            QMessageBox.warning(self, "Item Kosong", "Baris tugas tidak lengkap. Refresh data.")
            return

        task_id = judul_item.data(Qt.ItemDataRole.UserRole)  # ← pastikan ini digunakan
        if not task_id:
            QMessageBox.warning(self, "ID Tugas Kosong", "Tugas tidak punya ID. Refresh data.")
            return

        current_status = self.tableWidget.item(selected_row, 2).text()
        if current_status == "Belum Selesai":
            tugas.tandai_selesai(self.conn,task_id)
            self.viewAttribute()
            QMessageBox.information(self, "Berhasil", "Tugas ditandai sebagai selesai.")
        else:
            QMessageBox.warning(self, "Sudah Selesai", "Tugas ini sudah selesai.")

    def fillAtrribute(self, user_id):
        judul = self.lineEditName.text()
        deskripsi = self.lineEditDesc.text()
        deadline = self.dateTimeEdit.dateTime().toString('dd/MM/yyyy HH:mm')
        status = False
        tugas_obj = tugas(judul, deskripsi, deadline, status)
        self.tugas_list.append(tugas_obj)
        tugas.simpan(self.conn, self.user_id, judul, deskripsi, deadline, status) 
        
        QMessageBox.information(self, "Success", f"Tugas '{tugas_obj.judul}' added successfully!")
        self.viewAttribute()
        self.stackedWidget.setCurrentIndex(1)

    def viewAttribute(self):
    # Ambil data tugas dari database untuk user yang sedang login
        if not hasattr(self, 'user_id'):
            QMessageBox.warning(self, "Error", "User belum login.")
            return
        self.tableWidget.setRowCount(0)  # Clear previous rows
        tasks = tugas.get_tasks(self.conn ,self.user_id)
        
        self.tableWidget.setRowCount(len(tasks))
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(["Judul", "Deadline", "Status"])
        for row, task in enumerate(tasks):
            #self.tableWidget.insertRow(row)

            item_judul = QTableWidgetItem(task[2])  # judul
            item_judul.setData(Qt.ItemDataRole.UserRole, task[0])  # simpan task.id

            item_deadline = QTableWidgetItem(task[4])
            item_status = QTableWidgetItem("Selesai" if task[5] else "Belum Selesai")

            self.tableWidget.setItem(row, 0, item_judul)
            self.tableWidget.setItem(row, 1, item_deadline)
            self.tableWidget.setItem(row, 2, item_status)
                
        if self.tableWidget.rowCount() > 0:
            self.tableWidget.selectRow(0)
            
    def viewSelectedTugas(self):
        #self.stackedWidget.setCurrentIndex(3)
        selected_row = self.tableWidget.currentRow()
        if selected_row < 0:
        # Kosongkan detail view jika tidak ada yang dipilih
            self.NameMainPage.setText("Tidak ada tugas dipilih")
            self.DescriptionMainPage.setText("")
            self.DeadlineMainPage.setText("")
            return
            # Get tasks from DB to find the correct id and details
        tasks = tugas.get_tasks(self.conn, self.user_id)
        if selected_row < len(tasks):
            task = tasks[selected_row]
            # task: (id, user_id, judul, deskripsi, deadline, status)
            judul = task[2]
            deskripsi = task[3]
            deadline = task[4]
            status = "Selesai" if task[5] else "Belum Selesai"

            # Set details to the widgets in DetailedView
            self.NameMainPage.setText(judul)
            self.DescriptionMainPage.setText(deskripsi)
            self.DeadlineMainPage.setText(f"Deadline: {deadline} | Status: {status}")
        else:
            QMessageBox.warning(self, "Error", "Data tugas tidak ditemukan.")

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
            task_id = self.tableWidget.item(self.selected_row, 0).data(Qt.UserRole)
            judul = self.lineEdit.text()
            deskripsi = self.lineEdit_2.text()
            deadline = self.dateTimeEdit_2.dateTime().toString('dd/MM/yyyy HH:mm')

            tugas.edit_task(self.conn, task_id, judul=judul, deskripsi=deskripsi, deadline=deadline)
            self.viewAttribute()
            self.stackedWidget.setCurrentIndex(1)
            self.selected_row = None

    def deleteTugas(self):
        selected_indexes = self.tableWidget.selectionModel().selectedRows()

        if not selected_indexes:
            QMessageBox.warning(self, "Pilih Tugas", "Silakan pilih tugas terlebih dahulu.")
            return

        selected_row = selected_indexes[0].row()
        task_id = self.tableWidget.item(selected_row, 0).data(Qt.ItemDataRole.UserRole)

        reply = QMessageBox.question(
            self, "Hapus", "Apakah Anda yakin ingin menghapus tugas ini?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
        if reply == QMessageBox.StandardButton.Yes:
            if tugas.hapus(self.conn, task_id):
                self.viewAttribute()
                QMessageBox.information(self, "Sukses", "Tugas berhasil dihapus!")
            else:
                QMessageBox.warning(self, "Gagal", "Tugas tidak ditemukan.")
                
        # if not selected_indexes:
        #     QMessageBox.warning(self, "Pilih Tugas", "Silakan pilih tugas terlebih dahulu.")
        #     return

        

    def loginPage(self):
        username = self.lineEditUsername.text()
        password = self.lineEditPassword.text()
        user = self.auth.login(username, password)  # auth is your AuthSystem instance

        if user:
            self.user_id = user.id  # Store user id for session
            self.stackedWidget.setCurrentIndex(1)
            self.viewAttribute()  # Load user-specific tasks
            QMessageBox.information(self, "Login Berhasil", f"Selamat datang, {user.username}!")
        else:
            QMessageBox.warning(self, "Login Gagal", "Username/email atau password salah.")
        
    def registerUser(self):
        username = self.lineEditRegistUser.text()
        email = self.lineEditRegistEmail.text()
        password = self.lineEditRegistPass.text()

        if not username or not email or not password:
            QMessageBox.warning(self, "Error", "Semua field harus diisi.")
            return

        if self.auth.register(username, email, password):
            QMessageBox.information(self, "Success", "Registrasi berhasil!")
            self.stackedWidget.setCurrentIndex(0)
        else:
            QMessageBox.warning(self, "Error", "Registrasi gagal. Mungkin email sudah terdaftar.")
        
    def getDetail(self):
        selected_row = self.tableWidget.currentRow()
        if selected_row >= 0:
            # Get tasks from DB to find the correct id and details
            tasks = self.tugas_manager.get_tasks(self.user_id)
            if selected_row < len(tasks):
                task = tasks[selected_row]
                # task: (id, user_id, judul, deskripsi, deadline, status)
                judul = task[2]
                deskripsi = task[3]
                deadline = task[4]
                status = "Selesai" if task[5] else "Belum Selesai"

                # Set details to the widgets in DetailedView
                self.NameLabelDetail.setText(judul)
                self.DescriptionDetail.setText(deskripsi)
                self.DeadlineDetail.setText(f"Deadline: {deadline} | Status: {status}")
            else:
                QMessageBox.warning(self, "Error", "Data tugas tidak ditemukan.")
        else:
            QMessageBox.warning(self, "Pilih Tugas", "Silahkan pilih tugas terlebih dahulu.")

app = QApplication([])
apply_stylesheet(app, theme='dark_blue.xml')
# with open("cobacss.qss", "r") as f:
#     app.setStyleSheet(f.read())
window = MyWindow()
window.show()
app.exec()