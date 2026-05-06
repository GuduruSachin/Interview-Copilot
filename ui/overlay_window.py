from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt
from config.constants import OVERLAY_OPACITY

class OverlayWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_overlay()

    def init_overlay(self):
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint | 
            Qt.FramelessWindowHint | 
            Qt.WindowTransparentForInput
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowOpacity(OVERLAY_OPACITY)
        
        self.layout = QVBoxLayout()
        self.tip_label = QLabel("Waiting for context...")
        self.tip_label.setStyleSheet("""
            background-color: rgba(30, 30, 30, 200);
            color: #00FF00;
            font-size: 16px;
            padding: 15px;
            border-radius: 10px;
            border: 1px solid #444;
        """)
        self.layout.addWidget(self.tip_label)
        self.setLayout(self.layout)
