import sys

from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Светофор интерфейс1.ui', self)  # Загружаем дизайн
        self.btncrt.clicked.connect(self.createnote)
        self.btnmnl.clicked.connect(self.opennote)
        self.btnthm.clicked.connect(self.changetheme)


    def createnote(self):
        self.btncrt.setText("Chek1")

    def opennote(self):
        self.btnmnl.setText("Chek2")

    def changetheme(self):
        self.btnthm.setText("Chek3")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())