import sys
import sqlite3
from addEditCoffeeForm_ui import Ui_MainWindow as Ui_MainWindow2
from main_ui import Ui_MainWindow as Ui_MainWindow1
from PyQt6.QtWidgets import QMainWindow, QApplication, QTableWidgetItem


class Coffee(QMainWindow, Ui_MainWindow1):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.loadTable()
        self.add_btn.clicked.connect(self.add_item)
        self.edit_btn.clicked.connect(self.edit_item)

    def loadTable(self):
        con = sqlite3.connect('coffee.sqlite')
        cur = con.cursor()
        execute = cur.execute('SELECT * FROM coffee').fetchall()
        title = ['ID', 'название сорта', 'степень обжарки', 'молотый/в зернах', 'описание вкуса', 'цена',
                 'объем упаковки']
        self.tableWidget.setColumnCount(len(title))
        self.tableWidget.setHorizontalHeaderLabels(title)
        for i, elem in enumerate(execute):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.tableWidget.resizeColumnsToContents()

    def updateTable(self):
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(0)
        self.loadTable()

    def add_item(self):
        add_coffee_form = addEditCoffeeForm('add', self)
        add_coffee_form.show()

    def edit_item(self):
        edit_coffee_form = addEditCoffeeForm('edit', self)
        edit_coffee_form.show()


class addEditCoffeeForm(QMainWindow, Ui_MainWindow2):
    def __init__(self, message, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.message = message
        self.initUI()

    def initUI(self):
        if self.message == 'add':
            self.pushButton.clicked.connect(self.add)
        elif self.message == 'edit':
            self.pushButton.clicked.connect(self.edit)

    def add(self):
        flag = self.try_add()
        print(flag)
        if not flag:
            self.statusBar().showMessage('Не удалось добавить')
        elif flag:
            con = sqlite3.connect('coffee.sqlite')
            cur = con.cursor()
            a = int(self.lineEdit.text())
            b = self.lineEdit_2.text()
            c = self.lineEdit_3.text()
            d = self.lineEdit_4.text()
            e = self.lineEdit_5.text()
            f = int(self.lineEdit_6.text())
            g = int(self.lineEdit_7.text())
            cur.execute('INSERT INTO coffee VALUES (?, ?, ?, ?, ?, ?, ?)', (a, b, c, d, e, f, g))
            con.commit()
            self.parent().updateTable()
            self.close()

    def try_add(self):
        con = sqlite3.connect('coffee.sqlite')
        cur = con.cursor()
        elem = cur.execute('SELECT ID FROM coffee').fetchall()
        elem = [i[0] for i in elem]
        try:
            if int(self.lineEdit.text()) in elem or self.lineEdit.text() == '':
                raise Exception
            if int(self.lineEdit_6.text()) < 0 or self.lineEdit_6.text() == '':
                raise Exception
            if int(self.lineEdit_7.text()) < 0 or self.lineEdit_7.text() == '':
                raise Exception
            if self.lineEdit_2.text() == '':
                raise Exception
            if self.lineEdit_3.text() == '':
                raise Exception
            if self.lineEdit_4.text() == '':
                raise Exception
            if self.lineEdit_5.text() == '':
                raise Exception
            return True
        except Exception:
            return False

    def edit(self):
        flag = self.try_edit()
        if not flag:
            self.statusBar().showMessage('Не удалось отредактировать')
        elif flag:
            con = sqlite3.connect('coffee.sqlite')
            cur = con.cursor()
            a = int(self.lineEdit.text())
            b = self.lineEdit_2.text()
            c = self.lineEdit_3.text()
            d = self.lineEdit_4.text()
            e = self.lineEdit_5.text()
            f = int(self.lineEdit_6.text())
            g = int(self.lineEdit_7.text())
            cur.execute('DELETE FROM coffee WHERE ID == ?', (a,))
            cur.execute('INSERT INTO coffee VALUES (?, ?, ?, ?, ?, ?, ?)', (a, b, c, d, e, f, g))
            con.commit()
            self.parent().updateTable()
            self.close()

    def try_edit(self):
        con = sqlite3.connect('coffee.sqlite')
        cur = con.cursor()
        elem = cur.execute('SELECT ID FROM coffee').fetchall()
        elem = [i[0] for i in elem]
        try:
            if int(self.lineEdit.text()) not in elem or self.lineEdit.text() == '':
                raise Exception
            if int(self.lineEdit_6.text()) < 0 or self.lineEdit_6.text() == '':
                raise Exception
            if int(self.lineEdit_7.text()) < 0 or self.lineEdit_7.text() == '':
                raise Exception
            if self.lineEdit_2.text() == '':
                raise Exception
            if self.lineEdit_3.text() == '':
                raise Exception
            if self.lineEdit_4.text() == '':
                raise Exception
            if self.lineEdit_5.text() == '':
                raise Exception
            return True
        except Exception:
            return False


if __name__ == '__main__':
    app = QApplication(sys.argv)
    coffee = Coffee()
    coffee.show()
    sys.exit(app.exec())
