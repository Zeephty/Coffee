import sys
from PyQt6.QtWidgets import QMainWindow, QApplication, QTableWidgetItem
import sqlite3
from PyQt6 import uic


class AddEditCoffeeForm(QMainWindow):
    def __init__(self, parent, index=None):
        super().__init__()

        uic.loadUi("addEditCoffeeForm.ui", self)

        self.par = parent
        self.coffee_id = index

        if self.coffee_id is not None:
            self.pushButton.clicked.connect(self.upd_coffee)
            self.edit_elem()
        else:
            self.pushButton.clicked.connect(self.add_coffee)
    
    def edit_elem(self):
        con = sqlite3.connect("coffee.sqlite")
        cur = con.cursor()
        a = list(cur.execute(f"Select * from Coffee where Coffee.id = {self.coffee_id}").fetchall())[0]
        con.close()
        self.editName.setText(a[1])
        self.editStep.setText(str(a[2]))
        self.editMz.setText(a[3])
        self.editOpis.setText(a[4])
        self.EditMoney.setText(str(a[5]))
        self.editVolume.setText(a[6])

    def upd_coffee(self):
        if self.AddUpdItem():
            con = sqlite3.connect("coffee.sqlite")
            cur = con.cursor()
            cur.execute(f"""UPDATE Coffee set
                        name = '{self.editName.text()}', 
                        step = {self.editStep.text()}, 
                        mz = '{self.editMz.text()}', 
                        opis = '{self.editOpis.text()}', 
                        coin = {self.EditMoney.text()}, 
                        v = '{self.editVolume.text()}' where Coffee.id = {self.coffee_id};""").fetchall()
            con.commit()
            con.close()
            self.par.updTable()
            self.close()
        else:
            self.statusBar().showMessage("Форма заполненна некорректно")

    def add_coffee(self):
        if self.AddUpdItem():
            con = sqlite3.connect("coffee.sqlite")
            cur = con.cursor()
            text = f"""INSERT INTO Coffee(name, step, mz, opis, coin, v) 
                           VALUES('{self.editName.text()}', {self.editStep.text()}, '{self.editMz.text()}', 
                           '{self.editOpis.text()}', {self.EditMoney.text()}, '{self.editVolume.text()}');"""
            cur.execute(text).fetchall()
            con.commit()
            con.close()
            self.par.updTable()
            self.close()
        else:
            self.statusBar().showMessage("Форма заполненна некорректно")
            
    def AddUpdItem(self):
        name = self.editName.text()
        mz = self.editMz.text()
        opis = self.editOpis.text()
        step = self.editStep.text()
        volume = self.editVolume.text()
        money = self.EditMoney.text()

        if (name and mz and opis and step.isdigit() and volume and money.isdigit()):
            return True
        else:
            return False


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi("main.ui", self)

        self.con = sqlite3.connect("coffee.sqlite")
        self.cur = self.con.cursor()

        self.updTable()

        self.addButton.clicked.connect(self.add_item)
        self.updateButton.clicked.connect(self.update_item)

    def add_item(self):
        self.add_form = AddEditCoffeeForm(self)
        self.add_form.show()

    def update_item(self):
        a = set([self.tableWidget.item(i.row(), 0).text() for i in self.tableWidget.selectedIndexes()])
        if a:
            self.statusBar().showMessage("")
            self.update_form = AddEditCoffeeForm(self, list(a)[0])
            self.update_form.show()
        else:
            self.statusBar().showMessage("Не выделенно ни одного элемента")
        
    def updTable(self):
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