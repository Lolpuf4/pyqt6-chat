from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout,
    QPushButton, QLabel, QLineEdit, QMessageBox
)
from PyQt6.QtCore import QThread, pyqtSignal
import json
import datetime
import os
from protocol import *
from chat_window import ChatWindow



class LoginWorker(QThread):
    result = pyqtSignal(bool, str, str)  # success, msg, username

    def __init__(self, username, password, server_connection):
        super().__init__()
        self.username = username
        self.password = password
        self.server_connection = server_connection

    def run(self):
        success, msg = self.server_connection.try_login(self.username, self.password)
        self.result.emit(success, msg, self.username)

class LoginWindow(QWidget):
    def __init__(self, server_connection):
        super().__init__()
        self.server_connection = server_connection
        self.log_in_tries = 3
        self.worker = None

        self.init_ui()
        self.load_cookie()


    def init_ui(self):
        self.setWindowTitle("Login")
        self.setGeometry(300, 300, 300, 150)
        layout = QVBoxLayout(self)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.login_btn = QPushButton("Login")
        self.login_btn.clicked.connect(self.start_login)

        layout.addWidget(QLabel("Please log in"))
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_btn)

    def load_cookie(self):
        if os.path.exists("jsons/cookie.json"):
            f =  open("jsons/cookie.json", "r", encoding="UTF-8")
            data = json.load(f)
            f.close()

            last_login_date = datetime.date(*list(map(int, data["date"].split("/"))))
            today = datetime.date.today()
            if (today - last_login_date).days < 8:
                self.username_input.setText(data["username"])
                self.password_input.setText(data["password"])

    def start_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Error", "Please enter both username and password.")
            return

        # Disable button while logging in
        self.login_btn.setEnabled(False)
        self.login_btn.setText("Logging in...")

        # Run login in worker thread
        self.worker = LoginWorker(username, password, self.server_connection)
        self.worker.result.connect(self.handle_login_result)
        self.worker.start()

    def handle_login_result(self, success, msg, username):
        self.login_btn.setEnabled(True)
        self.login_btn.setText("Login")

        if success:
            chat_window = ChatWindow(username, self.server_connection)
            self.close()
        else:
            self.log_in_tries -= 1
            if self.log_in_tries <= 0:
                QMessageBox.critical(self, "Error", "Too many failed attempts.")
                self.close()
            else:
                QMessageBox.warning(self, "Login Failed", f"{msg}\nTries left: {self.log_in_tries}")