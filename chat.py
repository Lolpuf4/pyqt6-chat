import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTextEdit, QLabel, QLineEdit, QStackedWidget, QMessageBox
)
from PyQt6.QtGui import QTextCursor, QTextBlockFormat
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush

from login_window import LoginWindow
import socket
import json
import datetime
import os
from protocol.protocol import *

from connection import Connection
from login_window import LoginWindow

class App:
    def __init__(self):

        self.server_connection = Connection()
        self.login_window = LoginWindow(self.server_connection)
        self.login_window.show()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    chat = App()
    app.aboutToQuit.connect(chat.server_connection.disconnect)
    sys.exit(app.exec())
