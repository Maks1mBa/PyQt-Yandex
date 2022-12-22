import sys

import sqlite3
import calendar
from datetime import date
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtSql import QSqlDatabase
from PyQt5.QtCore import pyqtSignal

sun = False

class readWindow(QWidget):
    window_closed = pyqtSignal()

    def __init__(self, id):
        self.id = id
        global sun
        super(readWindow, self).__init__()
        uic.loadUi('Светофор интерфейс4.ui', self)
        if sun:
            self.setStyleSheet('background-color : white')
            self.label1.setStyleSheet('background-color : rgb(0, 0, 205); color : white')
            self.label2.setStyleSheet('background-color : rgb(0, 0, 205); color : white')
            self.label3.setStyleSheet('background-color : rgb(0, 0, 205); color : white')
            self.label4.setStyleSheet('background-color : rgb(0, 0, 205); color : white')
        else:
            self.setStyleSheet('background-color : rgb(160,160,160)')
            self.label1.setStyleSheet('background-color : rgb(180,170,160)')
            self.label2.setStyleSheet('background-color : rgb(180,170,160)')
            self.label3.setStyleSheet('background-color : rgb(180,170,160)')
            self.label4.setStyleSheet('background-color : rgb(180,170,160)')
        self.setWindowTitle('Создание/редактирование заметки')
        con = sqlite3.connect("notes.db")
        cur = con.cursor()
        result = cur.execute(f"""SELECT * FROM dnn
                                            WHERE id == {self.id}""").fetchall()
        result = result[0]
        self.datelab.setText(f'{result[1]}')
        self.shodeslab.setText(f'{result[3]}')
        self.fulldeslab.setText(f'{result[4]}')
        self.timinglab.setText(f'{result[2]}')
        con.close()

class editWindow(QWidget):
    window_closed = pyqtSignal()

    def __init__(self, id):
        self.id = id
        global sun
        super(editWindow, self).__init__()
        uic.loadUi('Светофор интерфейс3.ui', self)
        if sun:
            self.setStyleSheet('background-color : white')
            self.btnedit2.setStyleSheet('background-color : rgb(178, 34, 34); color : white')
            self.label1.setStyleSheet('background-color : rgb(0, 0, 205); color : white')
            self.label2.setStyleSheet('background-color : rgb(0, 0, 205); color : white')
            self.label3.setStyleSheet('background-color : rgb(0, 0, 205); color : white')
            self.label4.setStyleSheet('background-color : rgb(0, 0, 205); color : white')
        else:
            self.setStyleSheet('background-color : rgb(160,160,160)')
            self.btnedit2.setStyleSheet('background-color : gray')
            self.label1.setStyleSheet('background-color : rgb(180,170,160)')
            self.label2.setStyleSheet('background-color : rgb(180,170,160)')
            self.label3.setStyleSheet('background-color : rgb(180,170,160)')
            self.label4.setStyleSheet('background-color : rgb(180,170,160)')
        self.setWindowTitle('Создание/редактирование заметки')
        self.btnedit2.clicked.connect(self.edit)
        con = sqlite3.connect("notes.db")
        cur = con.cursor()
        result = cur.execute(f"""SELECT * FROM dnn
                                            WHERE id == {self.id}""").fetchall()
        result = result[0]
        self.datenote.setText(f'{result[1]}')
        self.shortnote.setText(f'{result[3]}')
        self.fullnote.setText(f'{result[4]}')
        self.timbox.setValue(result[2])
        con.close()

    def edit(self):
        self.date = self.datenote.text()
        self.funo = self.fullnote.text()
        self.shno = self.shortnote.text()
        self.timi = self.timbox.text()
        self.con = sqlite3.connect("notes.db")
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('notes.db')
        db.open()
        cur = self.con.cursor()
        sqlite_insert_query = f"""UPDATE dnn SET date = '{self.date}', timing = '{self.timi}', shodes = '{self.shno}', 
        des = '{self.funo}' WHERE id = {self.id}"""
        cur.execute(sqlite_insert_query)
        self.con.commit()
        self.con.close()
        self.close()

    def closeEvent(self, event):
        self.window_closed.emit()
        event.accept()


class createWindow(QWidget):
    window_closed = pyqtSignal()

    def __init__(self):
        global sun
        super(createWindow, self).__init__()
        uic.loadUi('Светофор интерфейс2.ui', self)
        if sun:
            self.setStyleSheet('background-color : white')
            self.btnsave.setStyleSheet('background-color : rgb(178, 34, 34); color : white')
            self.label1.setStyleSheet('background-color : rgb(0, 0, 205); color : white')
            self.label2.setStyleSheet('background-color : rgb(0, 0, 205); color : white')
            self.label3.setStyleSheet('background-color : rgb(0, 0, 205); color : white')
            self.label4.setStyleSheet('background-color : rgb(0, 0, 205); color : white')
        else:
            self.setStyleSheet('background-color : rgb(160,160,160)')
            self.btnsave.setStyleSheet('background-color : gray')
            self.label1.setStyleSheet('background-color : rgb(180,170,160)')
            self.label2.setStyleSheet('background-color : rgb(180,170,160)')
            self.label3.setStyleSheet('background-color : rgb(180,170,160)')
            self.label4.setStyleSheet('background-color : rgb(180,170,160)')
        self.setWindowTitle('Создание/редактирование заметки')
        self.btnsave.clicked.connect(self.save)

    def closeEvent(self, event):
        self.window_closed.emit()
        event.accept()

    def save(self):
        self.date = self.datenote.text()
        self.funo = self.fullnote.text()
        self.shno = self.shortnote.text()
        self.timi = self.timbox.text()

        self.con = sqlite3.connect("notes.db")
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('notes.db')
        db.open()
        cur = self.con.cursor()
        sqlite_insert_query = f"""INSERT INTO dnn
                                  (date, shodes, des, timing)
                                  VALUES
                                  ('{self.date}', '{self.shno}', '{self.funo}', {self.timi});"""
        cur.execute(sqlite_insert_query)
        self.con.commit()
        self.con.close()
        self.close()


class Calendar(QMainWindow):
    def __init__(self):
        super().__init__()
        self.now = [int(str(date.today()).split('-')[2]),
                    int(str(date.today()).split('-')[1]),
                    int(str(date.today()).split('-')[0])]
        self.datch = None
        self.id = 0
        sqlite_connection = sqlite3.connect('notes.db')
        self.cursor = sqlite_connection.cursor()
        uic.loadUi('Светофор интерфейс1.ui', self)
        self.setWindowTitle('Календарь "Светофор"')
        self.list()
        self.btncrt.clicked.connect(self.createnote)
        self.btnmnl.clicked.connect(self.opennote)
        self.btnthm.clicked.connect(self.changetheme)
        self.btnlef.clicked.connect(self.left)
        self.btnrig.clicked.connect(self.right)
        self.btnchoice.clicked.connect(self.choice)
        self.edibtn.clicked.connect(self.editnote)
        self.moye.setText(f"{self.datnow(self.now)}")
        self.changetheme()

    def choice(self):
        if self.listWidget.currentItem() == None:
            return
        b = (self.listWidget.currentItem().text()).split()
        self.id = b[2][1:-1]
        con = sqlite3.connect("notes.db")
        cur = con.cursor()
        result = cur.execute(f"""SELECT * FROM dnn
                                    WHERE id == {self.id}""").fetchall()
        result = result[0]
        day = int(result[1].split('.')[0])
        mounth = int(result[1].split('.')[1])
        year = int(result[1].split('.')[2])
        timing = int(result[2])
        con.close()
        self.changetheme()
        self.changetheme()
        spisokred = []
        spisokora = []
        spisokgre = []
        for d in range(timing * 3):
            if d < timing:
                if mounth == self.now[1] and year == self.now[2]:
                    spisokred.append(day)
                day -= 1
                if day == 0:
                    mounth -= 1
                    if mounth == 0:
                        mounth = 12
                        year -= 1
                    day = calendar.monthrange(year, mounth)[1]
            elif d < timing * 2:
                if mounth == self.now[1] and year == self.now[2]:
                    spisokora.append(day)
                day -= 1
                if day == 0:
                    mounth -= 1
                    if mounth == 0:
                        mounth = 12
                        year -= 1
                    day = calendar.monthrange(year, mounth)[1]
            elif d < timing * 3:
                if mounth == self.now[1] and year == self.now[2]:
                    spisokgre.append(day)
                day -= 1
                if day == 0:
                    mounth -= 1
                    if mounth == 0:
                        mounth = 12
                        year -= 1
                    day = calendar.monthrange(year, mounth)[1]
        for i in spisokred:
            if i == 1:
                self.btnd1.setStyleSheet('background-color : red')
            elif i == 2:
                self.btnd2.setStyleSheet('background-color : red')
            elif i == 3:
                self.btnd3.setStyleSheet('background-color : red')
            elif i == 4:
                self.btnd4.setStyleSheet('background-color : red')
            elif i == 5:
                self.btnd5.setStyleSheet('background-color : red')
            elif i == 6:
                self.btnd6.setStyleSheet('background-color : red')
            elif i == 7:
                self.btnd7.setStyleSheet('background-color : red')
            elif i == 8:
                self.btnd8.setStyleSheet('background-color : red')
            elif i == 9:
                self.btnd9.setStyleSheet('background-color : red')
            elif i == 10:
                self.btnd10.setStyleSheet('background-color : red')
            elif i == 11:
                self.btnd11.setStyleSheet('background-color : red')
            elif i == 12:
                self.btnd12.setStyleSheet('background-color : red')
            elif i == 13:
                self.btnd13.setStyleSheet('background-color : red')
            elif i == 14:
                self.btnd14.setStyleSheet('background-color : red')
            elif i == 15:
                self.btnd15.setStyleSheet('background-color : red')
            elif i == 16:
                self.btnd16.setStyleSheet('background-color : red')
            elif i == 17:
                self.btnd17.setStyleSheet('background-color : red')
            elif i == 18:
                self.btnd18.setStyleSheet('background-color : red')
            elif i == 19:
                self.btnd19.setStyleSheet('background-color : red')
            elif i == 20:
                self.btnd20.setStyleSheet('background-color : red')
            elif i == 21:
                self.btnd21.setStyleSheet('background-color : red')
            elif i == 22:
                self.btnd22.setStyleSheet('background-color : red')
            elif i == 23:
                self.btnd23.setStyleSheet('background-color : red')
            elif i == 24:
                self.btnd24.setStyleSheet('background-color : red')
            elif i == 25:
                self.btnd25.setStyleSheet('background-color : red')
            elif i == 26:
                self.btnd26.setStyleSheet('background-color : red')
            elif i == 27:
                self.btnd27.setStyleSheet('background-color : red')
            elif i == 28:
                self.btnd28.setStyleSheet('background-color : red')
            elif i == 29:
                self.btnd29.setStyleSheet('background-color : red')
            elif i == 30:
                self.btnd30.setStyleSheet('background-color : red')
            elif i == 31:
                self.btnd31.setStyleSheet('background-color : red')
        for i in spisokora:
            if i == 1:
                self.btnd1.setStyleSheet('background-color : orange')
            elif i == 2:
                self.btnd2.setStyleSheet('background-color : orange')
            elif i == 3:
                self.btnd3.setStyleSheet('background-color : orange')
            elif i == 4:
                self.btnd4.setStyleSheet('background-color : orange')
            elif i == 5:
                self.btnd5.setStyleSheet('background-color : orange')
            elif i == 6:
                self.btnd6.setStyleSheet('background-color : orange')
            elif i == 7:
                self.btnd7.setStyleSheet('background-color : orange')
            elif i == 8:
                self.btnd8.setStyleSheet('background-color : orange')
            elif i == 9:
                self.btnd9.setStyleSheet('background-color : orange')
            elif i == 10:
                self.btnd10.setStyleSheet('background-color : orange')
            elif i == 11:
                self.btnd11.setStyleSheet('background-color : orange')
            elif i == 12:
                self.btnd12.setStyleSheet('background-color : orange')
            elif i == 13:
                self.btnd13.setStyleSheet('background-color : orange')
            elif i == 14:
                self.btnd14.setStyleSheet('background-color : orange')
            elif i == 15:
                self.btnd15.setStyleSheet('background-color : orange')
            elif i == 16:
                self.btnd16.setStyleSheet('background-color : orange')
            elif i == 17:
                self.btnd17.setStyleSheet('background-color : orange')
            elif i == 18:
                self.btnd18.setStyleSheet('background-color : orange')
            elif i == 19:
                self.btnd19.setStyleSheet('background-color : orange')
            elif i == 20:
                self.btnd20.setStyleSheet('background-color : orange')
            elif i == 21:
                self.btnd21.setStyleSheet('background-color : orange')
            elif i == 22:
                self.btnd22.setStyleSheet('background-color : orange')
            elif i == 23:
                self.btnd23.setStyleSheet('background-color : orange')
            elif i == 24:
                self.btnd24.setStyleSheet('background-color : orange')
            elif i == 25:
                self.btnd25.setStyleSheet('background-color : orange')
            elif i == 26:
                self.btnd26.setStyleSheet('background-color : orange')
            elif i == 27:
                self.btnd27.setStyleSheet('background-color : orange')
            elif i == 28:
                self.btnd28.setStyleSheet('background-color : orange')
            elif i == 29:
                self.btnd29.setStyleSheet('background-color : orange')
            elif i == 30:
                self.btnd30.setStyleSheet('background-color : orange')
            elif i == 31:
                self.btnd31.setStyleSheet('background-color : orange')
        for i in spisokgre:
            if i == 1:
                self.btnd1.setStyleSheet('background-color : green')
            elif i == 2:
                self.btnd2.setStyleSheet('background-color : green')
            elif i == 3:
                self.btnd3.setStyleSheet('background-color : green')
            elif i == 4:
                self.btnd4.setStyleSheet('background-color : green')
            elif i == 5:
                self.btnd5.setStyleSheet('background-color : green')
            elif i == 6:
                self.btnd6.setStyleSheet('background-color : green')
            elif i == 7:
                self.btnd7.setStyleSheet('background-color : green')
            elif i == 8:
                self.btnd8.setStyleSheet('background-color : green')
            elif i == 9:
                self.btnd9.setStyleSheet('background-color : green')
            elif i == 10:
                self.btnd10.setStyleSheet('background-color : green')
            elif i == 11:
                self.btnd11.setStyleSheet('background-color : green')
            elif i == 12:
                self.btnd12.setStyleSheet('background-color : green')
            elif i == 13:
                self.btnd13.setStyleSheet('background-color : green')
            elif i == 14:
                self.btnd14.setStyleSheet('background-color : green')
            elif i == 15:
                self.btnd15.setStyleSheet('background-color : green')
            elif i == 16:
                self.btnd16.setStyleSheet('background-color : green')
            elif i == 17:
                self.btnd17.setStyleSheet('background-color : green')
            elif i == 18:
                self.btnd18.setStyleSheet('background-color : green')
            elif i == 19:
                self.btnd19.setStyleSheet('background-color : green')
            elif i == 20:
                self.btnd20.setStyleSheet('background-color : green')
            elif i == 21:
                self.btnd21.setStyleSheet('background-color : green')
            elif i == 22:
                self.btnd22.setStyleSheet('background-color : green')
            elif i == 23:
                self.btnd23.setStyleSheet('background-color : green')
            elif i == 24:
                self.btnd24.setStyleSheet('background-color : green')
            elif i == 25:
                self.btnd25.setStyleSheet('background-color : green')
            elif i == 26:
                self.btnd26.setStyleSheet('background-color : green')
            elif i == 27:
                self.btnd27.setStyleSheet('background-color : green')
            elif i == 28:
                self.btnd28.setStyleSheet('background-color : green')
            elif i == 29:
                self.btnd29.setStyleSheet('background-color : green')
            elif i == 30:
                self.btnd30.setStyleSheet('background-color : green')
            elif i == 31:
                self.btnd31.setStyleSheet('background-color : green')

    def list(self):
        self.listWidget.clear()
        con = sqlite3.connect("notes.db")
        cur = con.cursor()
        result = cur.execute("""SELECT * FROM dnn
                            WHERE id > 0""").fetchall()
        for elem in result:
            melen = []
            melen.append(str(elem[1]))
            melen.append(str(elem[3]))
            melen.append(f'({elem[0]})')
            self.listWidget.addItem(" ".join(melen))
        con.close()

    def left(self):
        self.now[1] -= 1
        if self.now[1] == 0:
            self.now[1] = 12
            self.now[2] -= 1
        self.moye.setText(f"{self.datnow(self.now)}")
        self.changetheme()
        self.changetheme()
        if self.datch != None:
            self.choice()

    def right(self):
        self.now[1] += 1
        if self.now[1] == 13:
            self.now[1] = 1
            self.now[2] += 1
        self.moye.setText(f"{self.datnow(self.now)}")
        self.changetheme()
        self.changetheme()
        if self.datch != None:
            self.choice()

    def datnow(self, data):
        mounths = {'1': 'Январь',
                   '2': 'Февраль',
                   '3': 'Март',
                   '4': 'Апрель',
                   '5': 'Май',
                   '6': 'Июнь',
                   '7': 'Июль',
                   '8': 'Август',
                   '9': 'Сентябрь',
                   '10': 'Октябрь',
                   '11': 'Ноябрь',
                   '12': 'Декабрь'}
        return f'{mounths[str(data[1])]} {data[2]}'

    def createnote(self):
        self.cw = createWindow()
        self.cw.window_closed.connect(self.list)
        self.cw.show()

    def opennote(self):
        self.re = readWindow(self.id)
        self.re.show()

    def editnote(self):
        self.ew = editWindow(self.id)
        self.ew.window_closed.connect(self.list)
        self.ew.show()
        pass

    def changetheme(self):
        global sun
        if sun:
            self.btnlef.setStyleSheet('background-color : gray')
            self.btnrig.setStyleSheet('background-color : gray')
            self.btnthm.setStyleSheet('background-color : gray')
            self.btncrt.setStyleSheet('background-color : gray')
            self.edibtn.setStyleSheet('background-color : gray')
            self.btnmnl.setStyleSheet('background-color : gray')
            self.centralwidget.setStyleSheet('background-color : rgb(160,160,160)')
            self.listWidget.setStyleSheet('background-color : rgb(160,170,160)')
            self.moye.setStyleSheet('background-color : rgb(180,170,160)')
            self.listtittle.setStyleSheet('background-color : rgb(180,170,160)')
            self.btnd1.setStyleSheet('background-color : rgb(180,170,160)')
            self.btnd2.setStyleSheet('background-color : rgb(180,170,160)')
            self.btnd3.setStyleSheet('background-color : rgb(180,170,160)')
            self.btnd4.setStyleSheet('background-color : rgb(180,170,160)')
            self.btnd5.setStyleSheet('background-color : rgb(180,170,160)')
            self.btnd6.setStyleSheet('background-color : rgb(180,170,160)')
            self.btnd7.setStyleSheet('background-color : rgb(180,170,160)')
            self.btnd8.setStyleSheet('background-color : rgb(180,170,160)')
            self.btnd9.setStyleSheet('background-color : rgb(180,170,160)')
            self.btnd10.setStyleSheet('background-color : rgb(180,170,160)')
            self.btnd11.setStyleSheet('background-color : rgb(180,170,160)')
            self.btnd12.setStyleSheet('background-color : rgb(180,170,160)')
            self.btnd13.setStyleSheet('background-color : rgb(180,170,160)')
            self.btnd14.setStyleSheet('background-color : rgb(180,170,160)')
            self.btnd15.setStyleSheet('background-color : rgb(180,170,160)')
            self.btnd16.setStyleSheet('background-color : rgb(180,170,160)')
            self.btnd17.setStyleSheet('background-color : rgb(180,170,160)')
            self.btnd18.setStyleSheet('background-color : rgb(180,170,160)')
            self.btnd19.setStyleSheet('background-color : rgb(180,170,160)')
            self.btnd20.setStyleSheet('background-color : rgb(180,170,160)')
            self.btnd21.setStyleSheet('background-color : rgb(180,170,160)')
            self.btnd22.setStyleSheet('background-color : rgb(180,170,160)')
            self.btnd23.setStyleSheet('background-color : rgb(180,170,160)')
            self.btnd24.setStyleSheet('background-color : rgb(180,170,160)')
            self.btnd25.setStyleSheet('background-color : rgb(180,170,160)')
            self.btnd26.setStyleSheet('background-color : rgb(180,170,160)')
            self.btnd27.setStyleSheet('background-color : rgb(180,170,160)')
            self.btnd28.setStyleSheet('background-color : rgb(180,170,160)')
            if self.days() >= 29:
                self.btnd29.setStyleSheet('background-color : rgb(180,170,160)')
            else:
                self.btnd29.setStyleSheet('background-color : rgb(160,160,160); color: rgb(160,160,160)')
            if self.days() >= 30:
                self.btnd30.setStyleSheet('background-color : rgb(180,170,160)')
            else:
                self.btnd30.setStyleSheet('background-color : rgb(160,160,160); color: rgb(160,160,160)')
            if self.days() == 31:
                self.btnd31.setStyleSheet('background-color : rgb(180,170,160)')
            else:
                self.btnd31.setStyleSheet('background-color : rgb(160,160,160); color: rgb(160,160,160)')
            sun = False
        else:
            self.btnlef.setStyleSheet('background-color : rgb(178, 34, 34); color : white')
            self.btnrig.setStyleSheet('background-color : rgb(178, 34, 34); color : white')
            self.btnthm.setStyleSheet('background-color : rgb(178, 34, 34); color : white')
            self.btncrt.setStyleSheet('background-color : rgb(178, 34, 34); color : white')
            self.btnmnl.setStyleSheet('background-color : rgb(178, 34, 34); color : white')
            self.edibtn.setStyleSheet('background-color : rgb(178, 34, 34); color : white')
            self.centralwidget.setStyleSheet('background-color : white')
            self.listWidget.setStyleSheet('background-color : white')
            self.moye.setStyleSheet('background-color : rgb(0, 0, 205); color : white')
            self.listtittle.setStyleSheet('background-color : rgb(0, 0, 205); color : white')
            self.btnd1.setStyleSheet('background-color : rgb(180,100,160)')
            self.btnd2.setStyleSheet('background-color : rgb(180,100,160)')
            self.btnd3.setStyleSheet('background-color : rgb(180,100,160)')
            self.btnd4.setStyleSheet('background-color : rgb(180,100,160)')
            self.btnd5.setStyleSheet('background-color : rgb(180,100,160)')
            self.btnd6.setStyleSheet('background-color : rgb(180,100,160)')
            self.btnd7.setStyleSheet('background-color : rgb(180,100,160)')
            self.btnd8.setStyleSheet('background-color : rgb(180,100,160)')
            self.btnd9.setStyleSheet('background-color : rgb(180,100,160)')
            self.btnd10.setStyleSheet('background-color : rgb(180,100,160)')
            self.btnd11.setStyleSheet('background-color : rgb(180,100,160)')
            self.btnd12.setStyleSheet('background-color : rgb(180,100,160)')
            self.btnd13.setStyleSheet('background-color : rgb(180,100,160)')
            self.btnd14.setStyleSheet('background-color : rgb(180,100,160)')
            self.btnd15.setStyleSheet('background-color : rgb(180,100,160)')
            self.btnd16.setStyleSheet('background-color : rgb(180,100,160)')
            self.btnd17.setStyleSheet('background-color : rgb(180,100,160)')
            self.btnd18.setStyleSheet('background-color : rgb(180,100,160)')
            self.btnd19.setStyleSheet('background-color : rgb(180,100,160)')
            self.btnd20.setStyleSheet('background-color : rgb(180,100,160)')
            self.btnd21.setStyleSheet('background-color : rgb(180,100,160)')
            self.btnd22.setStyleSheet('background-color : rgb(180,100,160)')
            self.btnd23.setStyleSheet('background-color : rgb(180,100,160)')
            self.btnd24.setStyleSheet('background-color : rgb(180,100,160)')
            self.btnd25.setStyleSheet('background-color : rgb(180,100,160)')
            self.btnd26.setStyleSheet('background-color : rgb(180,100,160)')
            self.btnd27.setStyleSheet('background-color : rgb(180,100,160)')
            self.btnd28.setStyleSheet('background-color : rgb(180,100,160)')
            self.btnd29.setStyleSheet('background-color : rgb(180,100,160)')
            self.btnd30.setStyleSheet('background-color : rgb(180,100,160)')
            self.btnd31.setStyleSheet('background-color : rgb(180,100,160)')
            if self.days() >= 29:
                self.btnd29.setStyleSheet('background-color : rgb(180,100,160)')
            else:
                self.btnd29.setStyleSheet('background-color : white; color: white')
            if self.days() >= 30:
                self.btnd30.setStyleSheet('background-color : rgb(180,100,160)')
            else:
                self.btnd30.setStyleSheet('background-color : white; color: white')
            if self.days() == 31:
                self.btnd31.setStyleSheet('background-color : rgb(180,100,160)')
            else:
                self.btnd31.setStyleSheet('background-color : white; color: white')
            sun = True

    def days(self):
        return calendar.monthrange(self.now[2], self.now[1])[1]


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Calendar()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
