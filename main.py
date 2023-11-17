import sys
import sqlite3
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi
from home import Home
import hashlib

class Login(QDialog):
    def __init__(self):
        super(Login,self).__init__()
        loadUi("login.ui",self)
        self.login.clicked.connect(self.loginfunction)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.createacc.clicked.connect(self.createaccount)

    def loginfunction(self):
        username = self.username.text()
        password = self.password.text()
        hashval = hashlib.sha256()
        hashval.update(password.encode())
        hashpassword = hashval.hexdigest()
        if not username or not password:
            self.error.setText("Please Fill In All Fields")
        else:
            conn = sqlite3.connect("main.db")
            cur = conn.cursor()
            query = "SELECT Password FROM users WHERE Username = ?"
            cur.execute(query,(username,))
            result = cur.fetchone()
            cur.close()
            conn.close()
            if result is None:
                self.error.setText("The Username Is Not Found")
            else:
                passresult = result[0]
                if passresult == hashpassword:
                    self.error.setText("")
                    self._new_window = Home(username)
                    self._new_window.show()
                else:
                    self.error.setText("The Password Is Incorrect")

    def createaccount(self):
        createacc= Create()
        widget.addWidget(createacc)
        widget.setCurrentIndex(widget.currentIndex()+1)


class Create(QDialog):
    def __init__(self):
        super(Create,self).__init__()
        loadUi("createacc.ui",self)
        self.signupbutton.clicked.connect(self.createacc)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmpass.setEchoMode(QtWidgets.QLineEdit.Password)
        self.back.clicked.connect(self.gotologin)

    def createacc(self):
        username = self.username.text()
        password = self.password.text()
        confirmpass = self.confirmpass.text()
        email = self.email.text()
        ID = self.id.text()
        balance = self.balance.text()
        buypower = self.power.text()
        hashval = hashlib.sha256()
        hashval.update(password.encode())
        hashpassword = hashval.hexdigest()

        if username == "" or password == "" or confirmpass == "" or email == "" or ID == "" or balance == "" or buypower == "":
            self.error.setText("Please Complete All Fields To Proceed")
        elif password != confirmpass:
            self.error.setText("Passwords Do Not Match")
        else:
            conn = sqlite3.connect("main.db")
            cur = conn.cursor()
            q = "INSERT INTO users(UserID,Username,Password,Email,Balance,BuyPower) VALUES (?,?,?,?,?,?)"
            cur.execute(q,(int(ID),username,hashpassword,email,balance,buypower))
            conn.commit()
            conn.close()
            self.error.setText("Success! Account Has Been Created")

    def gotologin(self):
        login = Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    login = Login()
    widget = QStackedWidget()
    widget.addWidget(login)
    widget.setFixedHeight(900)
    widget.setFixedWidth(1600)
    widget.show()
    sys.exit(app.exec_())
