from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem
from PyQt6.QtCore import QDateTime
from PBOTest import tugas
import sys
from datetime import datetime

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("UItest.ui", self)
        self.stackedWidget.setCurrentIndex(0)
        self.pushButtonLOGIN.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.pushButtonFILL.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))

        self.pushButtonSubmit.clicked.connect(self.fillAtrribute)
        self.pushButtonView.clicked.connect(self.viewAttribute)
        self.pushButtonBack.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.pushButtonBack_2.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))

        self.pushButtonEdit.clicked.connect(self.editTugas)
        self.pushButtonSave.clicked.connect(self.saveEditedTugas)
        self.pushButtonDelete.clicked.connect(self.deleteTugas)

        self.tugas_list = []  # Store multiple tugas objects
        self.selected_row = None  # Track which row is being edited

    def fillAtrribute(self):
        judul = self.lineEditName.text()
        deskripsi = self.lineEditDesc.text()
        deadline = self.dateTimeEdit.dateTime().toString('dd/MM/yyyy HH:mm')
        status = False

        tugas_obj = tugas(judul, deskripsi, deadline, status)
        self.tugas_list.append(tugas_obj)
        with open("tugas_data.txt", "a", encoding="utf-8") as f:
            f.write(f"{tugas_obj.judul}\n{tugas_obj.deskripsi}\n{tugas_obj.deadline}\n{tugas_obj.status}\n--------------------------\n")
        QMessageBox.information(self, "Success", f"Tugas '{tugas_obj.judul}' added successfully!")
        self.stackedWidget.setCurrentIndex(1)

    def viewAttribute(self):
        # Load tugas objects from file if not already loaded
        if not self.tugas_list:
            try:
                with open("tugas_data.txt", "r", encoding="utf-8") as f:
                    lines = f.read().split("--------------------------\n")
                    for entry in lines:
                        if entry.strip():
                            parts = entry.strip().split("\n")
                            if len(parts) >= 4:
                                judul = parts[0]
                                deskripsi = parts[1]
                                deadline = parts[2]
                                status = parts[3] == "True"
                                tugas_obj = tugas(judul, deskripsi, deadline, status)
                                self.tugas_list.append(tugas_obj)
            except FileNotFoundError:
                pass

        # Fill the table widget
        self.tableWidget.setRowCount(len(self.tugas_list))
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setHorizontalHeaderLabels(["Judul", "Deskripsi", "Deadline", "Status"])

        for row, t in enumerate(self.tugas_list):
            self.tableWidget.setItem(row, 0, QTableWidgetItem(t.get_Judul()))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(t.get_Deskripsi()))
            self.tableWidget.setItem(row, 2, QTableWidgetItem(t.get_Deadline()))
            status_text = "Selesai" if t.get_Status() else "Belum Selesai"
            self.tableWidget.setItem(row, 3, QTableWidgetItem(status_text))

        # Optionally, still fill the QTextBrowser as before
        if self.tugas_list:
            display_text = ""
            for idx, t in enumerate(self.tugas_list, 1):
                display_text += (
                    f"Tugas {idx}:\n"
                    f"  Judul: {t.get_Judul()}\n"
                    f"  Deskripsi: {t.get_Deskripsi()}\n"
                    f"  Deadline: {t.get_Deadline()}\n"
                    f"  Status: {'Selesai' if t.get_Status() else 'Belum Selesai'}\n\n"
                )
            self.textBrowser.setPlainText(display_text)
        else:
            self.textBrowser.setPlainText("Belum ada tugas yang dibuat.")

    def editTugas(self):
        self.stackedWidget.setCurrentIndex(4)
        selected_row = self.tableWidget.currentRow()
        if selected_row >= 0:
            self.selected_row = selected_row
            # Fill edit fields with current values
            self.lineEdit.setText(self.tableWidget.item(selected_row, 0).text())
            self.lineEdit_2.setText(self.tableWidget.item(selected_row, 1).text())
            deadline_str = self.tableWidget.item(selected_row, 2).text()
            dt = QDateTime.fromString(deadline_str, 'dd/MM/yyyy HH:mm')
            self.dateTimeEdit_2.setDateTime(dt)

    def saveEditedTugas(self):
        if self.selected_row is not None:
            # Get new values from edit fields
            new_judul = self.lineEdit.text()
            new_deskripsi = self.lineEdit_2.text()
            new_deadline = self.dateTimeEdit_2.dateTime().toString('dd/MM/yyyy HH:mm')
            # Update object in list
            t = self.tugas_list[self.selected_row]
            t.set_Judul(new_judul)
            t.set_Deskripsi(new_deskripsi)
            t.set_Deadline(new_deadline)
            # Update table
            self.tableWidget.setItem(self.selected_row, 0, QTableWidgetItem(new_judul))
            self.tableWidget.setItem(self.selected_row, 1, QTableWidgetItem(new_deskripsi))
            self.tableWidget.setItem(self.selected_row, 2, QTableWidgetItem(new_deadline))
            status_text = "Selesai" if t.get_Status() else "Belum Selesai"
            self.tableWidget.setItem(self.selected_row, 3, QTableWidgetItem(status_text))
            # Save all tasks to file
            with open("tugas_data.txt", "w", encoding="utf-8") as f:
                for tugas_obj in self.tugas_list:
                    f.write(f"{tugas_obj.get_Judul()}\n{tugas_obj.get_Deskripsi()}\n{tugas_obj.get_Deadline()}\n{tugas_obj.get_Status()}\n--------------------------\n")
            QMessageBox.information(self, "Success", "Tugas berhasil diubah!")
            self.stackedWidget.setCurrentIndex(1)
            self.selected_row = None

    def deleteTugas(self):
        selected_row = self.tableWidget.currentRow()
        if selected_row >= 0:
            response = QMessageBox.question(self, "Delete", "Apakah Anda yakin ingin menghapus tugas ini?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if response == QMessageBox.StandardButton.Yes:
                del self.tugas_list[selected_row]
                self.tableWidget.removeRow(selected_row)
                QMessageBox.information(self, "Success", "Tugas berhasil dihapus!")
                # Save updated list to file
                with open("tugas_data.txt", "w", encoding="utf-8") as f:
                    for tugas_obj in self.tugas_list:
                        f.write(f"{tugas_obj.get_Judul()}\n{tugas_obj.get_Deskripsi()}\n{tugas_obj.get_Deadline()}\n{tugas_obj.get_Status()}\n--------------------------\n")

app = QApplication([])
window = MyWindow()
window.show()
app.exec()