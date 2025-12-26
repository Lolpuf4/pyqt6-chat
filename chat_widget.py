from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout,
    QTextEdit, QLabel, QLineEdit
)
from PyQt6.QtGui import QTextCursor, QTextBlockFormat
from PyQt6.QtCore import Qt




class ChatWidget(QWidget):
    def __init__(self, user, chat_history):
        super().__init__()
        self.user = user
        self.chat_history = chat_history  # list of {"sender":..., "text":...}
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)

        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("Type a message...")

        layout.addWidget(QLabel(f"Chat with {self.user}"))
        layout.addWidget(self.chat_display)
        layout.addWidget(self.input_box)

        self.input_box.returnPressed.connect(self.send_message)

        self.update_chat_display()


    def update_chat_display(self):
        self.chat_display.clear()
        cursor = self.chat_display.textCursor()

        for msg in self.chat_history["msgs"]:
            sender = msg["message_history.senderID"]
            text = msg["messages.text"]

            block_format = QTextBlockFormat()
            if sender == self.chat_history["senderID"]:
                block_format.setAlignment(Qt.AlignmentFlag.AlignRight)
            else:
                block_format.setAlignment(Qt.AlignmentFlag.AlignLeft)

            cursor.insertBlock(block_format)

            html = f"""
            <div style="
                background-color:{'#DCF8C6' if sender == self.chat_history['senderID'] else '#FFFFFF'};
                color: white;
                border: 1px solid #ccc;
                border-radius: 12px;
                padding: 8px 12px;
                margin: 6px;
                max-width: 60%;
                font-size: 14px;
            ">
            <b>{sender}</b><br>{text}
            </div>
            """

            cursor.insertHtml(html)


        self.chat_display.moveCursor(QTextCursor.MoveOperation.End)

    def send_message(self):
        print(12)
        text = self.input_box.text().strip()
        print(text)
        if not text:
            return

        #self.chat_history.append({"sender": "You", "text": text})
        sender = self.chat_history["senderID"]
        print(self.user)
        print(self.chat_history)
        self.chat_history["msgs"].append({'messages.text': text, 'messages.date': '15/12/25', 'messages.time': '16:39:31', 'users.username': self.user, 'message_history.senderID': sender, 'message_history.receiverID': '2'})
        print(self.chat_history)
        self.input_box.clear()
        self.update_chat_display()