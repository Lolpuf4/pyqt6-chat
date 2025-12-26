from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush


class TextBubble(QWidget):
    def __init__(self, text, parent = None):
        super().__init__(parent)

        self.label = QLabel(text)
        self.label.setStyleSheet("font-size: 14px;")

        layout = QHBoxLayout(self)
        layout.addWidget(self.label)
        layout.setContentsMargins(12, 8, 12, 8)  # padding inside bubble

        self.setLayout(layout)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Bubble color + border
        bubble_color = QColor(230, 240, 255)
        border_color = QColor(150, 170, 200)

        rect = self.rect().adjusted(1, 1, -1, -1)

        painter.setBrush(QBrush(bubble_color))
        painter.setPen(QPen(border_color, 2))

        painter.drawRoundedRect(rect, 12, 12)