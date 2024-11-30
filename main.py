import sys
from PyQt6.QtWidgets import QMainWindow, QApplication, QTableWidgetItem
import sqlite3
from PyQt6 import uic

 
class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(0, 0, 400, 400)
        self.setMouseTracking(True)

        uic.loadUi("main.ui", self)

        self.con = sqlite3.connect("coffee.sqlite")
        self.cur = self.con.cursor()

        a = list(self.cur.execute("select * from Coffee"))

        self.tableWidget.setRowCount(len(a))
        self.tableWidget.setColumnCount(7)

        self.tableWidget.setHorizontalHeaderLabels(["ID", "название сорта", "степень обжарки", 
                                                    "молотый/в зернах", "описание вкуса", "цена", "объем упаковки"])
        for i, elem in enumerate(a):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))

 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())