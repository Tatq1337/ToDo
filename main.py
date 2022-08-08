from PyQt5 import QtCore, QtGui, QtWidgets
import time
import sqlite3

conn = sqlite3.connect('todoDB.db')
cursor = conn.cursor()

cursor.execute("""
        CREATE TABLE if not exists todo_list(
        list_item text
        )
        """)

conn.commit()
conn.close()


class Ui_ToDoList(object):
    def setupUi(self, ToDoList):
        ToDoList.setObjectName("ToDoList")
        ToDoList.resize(801, 461)
        ToDoList.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.centralwidget = QtWidgets.QWidget(ToDoList)
        self.centralwidget.setObjectName("centralwidget")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(20, 120, 761, 281))
        self.listWidget.setStyleSheet("background-color: rgb(234, 234, 234);")
        self.listWidget.setObjectName("listWidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(20, 70, 761, 51))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.Add_to_list = QtWidgets.QPushButton(self.widget, clicked=lambda: self.add_item())
        self.Add_to_list.setStyleSheet("background-color: rgb(234, 234, 234);")
        self.Add_to_list.setObjectName("Add_to_list")
        self.horizontalLayout.addWidget(self.Add_to_list)
        self.Delete_from_list = QtWidgets.QPushButton(self.widget, clicked=lambda: self.delete_item())
        self.Delete_from_list.setStyleSheet("background-color: rgb(234, 234, 234);")
        self.Delete_from_list.setObjectName("Delete_from_list")
        self.horizontalLayout.addWidget(self.Delete_from_list)
        self.Clear_the_list = QtWidgets.QPushButton(self.widget, clicked=lambda: self.clear())
        self.Clear_the_list.setStyleSheet("background-color: rgb(234, 234, 234);")
        self.Clear_the_list.setObjectName("Clear_the_list")
        self.horizontalLayout.addWidget(self.Clear_the_list)
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(20, 20, 761, 41))
        self.lineEdit.setStyleSheet("background-color: rgb(234, 234, 234);")
        self.lineEdit.setObjectName("lineEdit")
        ToDoList.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(ToDoList)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 801, 21))
        self.menubar.setObjectName("menubar")
        ToDoList.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(ToDoList)
        self.statusbar.setObjectName("statusbar")
        ToDoList.setStatusBar(self.statusbar)

        self.retranslateUi(ToDoList)
        QtCore.QMetaObject.connectSlotsByName(ToDoList)
        self.restore()

    def restore(self):
        conn = sqlite3.connect('todoDB.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM todo_list")
        records = cursor.fetchall()

        conn.commit()
        conn.close()

        for record in records:
            self.listWidget.addItem(str(record[0]))

    def add_item(self):
        item = self.lineEdit.text()
        self.listWidget.addItem(item)
        self.lineEdit.setText("")
        self.save_to_db()

    def delete_item(self):
        idx = self.listWidget.currentRow()
        self.listWidget.takeItem(idx)

    def clear(self):
        self.listWidget.clear()
        self.save_to_db()

    def save_to_db(self):
        conn = sqlite3.connect('todoDB.db')
        cursor = conn.cursor()
        items = []

        cursor.execute('DELETE FROM todo_list;', )

        for idx in range(self.listWidget.count()):
            items.append(self.listWidget.item(idx))

        for item in items:
            cursor.execute('INSERT INTO todo_list VALUES (:item)',
                           {
                               'item': item.text(),
                           }
                           )
        conn.commit()
        conn.close()

    def retranslateUi(self, ToDoList):
        _translate = QtCore.QCoreApplication.translate
        ToDoList.setWindowTitle(_translate("ToDoList", "ToDoList"))
        self.Add_to_list.setText(_translate("ToDoList", "Dodaj"))
        self.Delete_from_list.setText(_translate("ToDoList", "Usuń"))
        self.Clear_the_list.setText(_translate("ToDoList", "Wyczyść listę"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ToDoList = QtWidgets.QMainWindow()
    ui = Ui_ToDoList()
    ui.setupUi(ToDoList)
    ToDoList.show()
    sys.exit(app.exec_())
