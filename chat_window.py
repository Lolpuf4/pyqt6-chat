from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QStackedWidget
)
from PyQt6.QtCore import QThread, pyqtSignal
import json
from protocol import *
from connection import Connection

from chat_widget import  ChatWidget



class GetData(QThread):
    result = pyqtSignal(dict)

    def __init__(self, server_connection):
        super().__init__()
        self.server_connection = server_connection


    def run(self):
        while self.server_connection.connection:
            information = self.server_connection.get_info()
            print(information)
            # if information == b"1":
            #     break
            # elif information == b"":
            #     continue
            self.result.emit(information)



class ChatWindow(QWidget):
    def __init__(self, username, server_connection):
        super().__init__()
        self.server_connection = server_connection
        self.start(username)

    def start(self, username):
        self.setWindowTitle(f"Chat - {username}")
        self.setGeometry(100, 100, 700, 500)

        self.new_msgs = {}
        self.chat_data = self.load_initial_messages()
        self.users = list(self.chat_data.keys())
        self.user_buttons = {}
        self.chat_widgets = {}

        self.init_ui()
        self.data_receiver = GetData(self.server_connection)
        self.data_receiver.result.connect(self.update_chat)
        self.data_receiver.start()
        self.current_user = None

        self.show()

    def update_chat(self, data):
        username = data["users.username"]
        self.chat_data[username]["msgs"].append(data)
        file = open("jsons/history.json", "w", encoding ="UTF-8")
        json.dump(self.chat_data, file)
        file.close()

        self.chat_widgets[username].update_chat_display()
        if self.current_user != username:
            last_msg = self.chat_data[username]["msgs"][-1]["messages.text"]
            self.new_msgs[username] = self.new_msgs.get(username, 0) + 1
            self.user_buttons[username].setText(f"{username} {last_msg} {self.new_msgs[username]}")






    def load_initial_messages(self):
        data = self.server_connection.get_info()

        file = open("jsons/history.json", "r", encoding ="UTF-8")
        local_history = json.load(file)
        file.close()
        for username in local_history:
            difference = len(data[username]["msgs"]) - len(local_history[username]["msgs"])
            self.new_msgs[username] = difference

        return data

    def init_ui(self):
        main_layout = QHBoxLayout(self)

        user_layout = QVBoxLayout()
        user_layout.addWidget(QLabel("Users"))

        for user in self.users:
            msgs = self.chat_data[user]["msgs"]
            last_msg = "No msgs" if not msgs else msgs[-1]["messages.text"]
            new_msg_count = f", {self.new_msgs[user]}" if self.new_msgs[user] > 0 else ""
            btn = QPushButton(f"{user}, {last_msg}{new_msg_count}")
            btn.clicked.connect(lambda checked=False, u=user: self.switch_user(u))
            user_layout.addWidget(btn)
            self.user_buttons[user] = btn

        user_layout.addStretch()

        self.chat_stack = QStackedWidget()
        initial_widget = ChatWidget("Choose chat", {"msgs": [], "senderID": "0"})
        self.chat_stack.addWidget(initial_widget)
        for user in self.users:
            chat_widget = ChatWidget(user, self.chat_data[user])
            self.chat_stack.addWidget(chat_widget)
            self.chat_widgets[user] = chat_widget

        main_layout.addLayout(user_layout, 1)
        main_layout.addWidget(self.chat_stack, 3)

        self.setLayout(main_layout)
        #self.switch_user(self.users[0])
        self.chat_stack.setCurrentWidget(initial_widget)

    def switch_user(self, user):
        for u, btn in self.user_buttons.items():
            if u == user:
                btn.setStyleSheet("background-color: lightblue; font-weight: bold;")
                self.current_user = user
            else:
                btn.setStyleSheet("")
        widget = self.chat_widgets.get(user)
        print(self.chat_data)
        if self.chat_data[user]["msgs"]:
            last_msg = self.chat_data[user]["msgs"][-1]["messages.text"]
        else:
            last_msg = "no msgs"
        if widget:
            self.chat_stack.setCurrentWidget(widget)
            self.user_buttons[user].setText(f"{user}, {last_msg}")
            self.new_msgs[user] = 0