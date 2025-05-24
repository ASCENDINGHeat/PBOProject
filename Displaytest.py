from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem
from PyQt6.QtCore import QDateTime
from PBOTest import tugas
from qt_material import apply_stylesheet

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("UItest.ui", self)
        self.stackedWidget.setCurrentIndex(0)
        self.pushButtonLOGIN.clicked.connect(lambda: (self.stackedWidget.setCurrentIndex(1), self.viewAttribute()))
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

        self.tugas_list = []
        self.selected_row = None

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

    def fillAtrribute(self):
        judul = self.lineEditName.text()
        deskripsi = self.lineEditDesc.text()
        deadline = self.dateTimeEdit.dateTime().toString('dd/MM/yyyy HH:mm')
        status = False
        tugas_obj = tugas(judul, deskripsi, deadline, status)
        self.tugas_list.append(tugas_obj)
        tugas.add_tugas(tugas_obj)
        QMessageBox.information(self, "Success", f"Tugas '{tugas_obj.judul}' added successfully!")
        self.stackedWidget.setCurrentIndex(1)
        self.viewAttribute()

    def viewAttribute(self):
        self.tugas_list = tugas.load_tugas()
        self.tableWidget.setRowCount(len(self.tugas_list))
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(["Judul", "Deadline","Status"])
        for row, t in enumerate(self.tugas_list):
            self.tableWidget.setItem(row, 0, QTableWidgetItem(t.judul))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(t.deadline))
            self.tableWidget.setItem(row, 2, QTableWidgetItem("Selesai" if t.status else "Belum Selesai"))
            
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

app = QApplication([])
apply_stylesheet(app, theme='dark_blue.xml')
window = MyWindow()
window.show()
app.exec()