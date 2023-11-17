import sys
import sqlite3
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi
import requests


class Home(QDialog):
    def __init__(self,username):
        super(Home,self).__init__()
        loadUi("homepage.ui",self)
        self.username = username
        self.back.clicked.connect(self.logout)
        self.updatebalance()
        self.convert.clicked.connect(self.currency)

    def logout(self):
        self.close()

    def updatebalance(self):
        conn = sqlite3.connect("main.db")
        cur = conn.cursor()
        query = "SELECT Balance FROM users WHERE Username = ?"
        cur.execute(query,(self.username,))
        result = cur.fetchone()
        conn.close()
        if result is None:
            self.namelbl.setText("User Not Found")
        else:
            balresult = result[0]
            self.balancelbl.setText("£"+balresult)

    def currency(self):
        amount = self.amount.text()
        fromc = self.fromc.text()
        toc = self.toc.text()
        if amount == "" or fromc == "" or toc == "":
            self.output.setText("")
        else:
            famount = float(amount)
            response = requests.get(f"https://api.frankfurter.app/latest?amount={famount}&from={fromc}&to={toc}")
            self.output.setText(str(response.json()['rates'][toc]))
