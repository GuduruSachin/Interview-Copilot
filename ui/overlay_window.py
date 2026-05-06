from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, QHBoxLayout, QDesktopWidget
from PyQt5.QtCore import Qt, QPoint
from utils.logger import get_logger

logger = get_logger(__name__)

class OverlayWindow(QWidget):
    def __init__(self, stop_callback=None):
        super().__init__()
        self.stop_callback = stop_callback
        self.old_pos = None
        self.setup_ui()

    def setup_ui(self):
        # Mandatory Window Properties
        self.setWindowFlags(
            Qt.FramelessWindowHint | 
            Qt.WindowStaysOnTopHint | 
            Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        # Uncomment for click-through in future:
        # self.setAttribute(Qt.WindowTransparentForInput)
        
        self.setWindowOpacity(0.85)

        # Default size and positioning
        self.setFixedSize(450, 300)
        self._position_bottom_right()

        layout = QVBoxLayout()
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(10)

        # Top Bar: Status and Stop Button
        top_bar_layout = QHBoxLayout()
        self.status_label = QLabel("● Listening")
        self.status_label.setStyleSheet("color: #00FFAA; font-weight: bold; font-size: 12px;")
        
        self.stop_btn = QPushButton("Stop")
        self.stop_btn.setFixedSize(50, 24)
        self.stop_btn.setStyleSheet("""
            QPushButton {
                background-color: #ff4444;
                color: white;
                border-radius: 4px;
                font-size: 11px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #ff6666; }
        """)
        if self.stop_callback:
            self.stop_btn.clicked.connect(self.stop_callback)

        top_bar_layout.addWidget(self.status_label)
        top_bar_layout.addStretch()
        top_bar_layout.addWidget(self.stop_btn)

        # Transcript Section
        transcript_label = QLabel("Interviewer")
        transcript_label.setStyleSheet("color: #AAAAAA; font-size: 11px; font-weight: bold;")
        
        self.transcript_area = QTextEdit()
        self.transcript_area.setReadOnly(True)
        self.transcript_area.setMaximumHeight(80)
        self.transcript_area.setStyleSheet("""
            QTextEdit {
                background-color: rgba(0, 0, 0, 100);
                color: white;
                border: 1px solid rgba(255, 255, 255, 30);
                border-radius: 6px;
                padding: 4px;
                font-size: 12px;
            }
        """)

        # AI Suggestion Section
        suggestion_label = QLabel("Suggestion")
        suggestion_label.setStyleSheet("color: #AAAAAA; font-size: 11px; font-weight: bold;")
        
        self.suggestion_area = QTextEdit()
        self.suggestion_area.setReadOnly(True)
        self.suggestion_area.setStyleSheet("""
            QTextEdit {
                background-color: rgba(0, 0, 0, 100);
                color: white;
                border: 1px solid rgba(255, 255, 255, 30);
                border-radius: 6px;
                padding: 4px;
                font-size: 13px;
                line-height: 1.4;
            }
        """)

        # Add to layout
        layout.addLayout(top_bar_layout)
        layout.addWidget(transcript_label)
        layout.addWidget(self.transcript_area)
        layout.addWidget(suggestion_label)
        layout.addWidget(self.suggestion_area)

        self.setLayout(layout)

        # Apply global style to overlay background
        self.setStyleSheet("""
            OverlayWindow {
                background-color: rgba(20, 20, 20, 180);
                border-radius: 12px;
            }
        """)

    def _position_bottom_right(self):
        screen = QDesktopWidget().availableGeometry()
        width = 450
        height = 300
        x = screen.width() - width - 20
        y = screen.height() - height - 40
        self.move(x, y)

    # --- Draggable Window Methods ---
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.old_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        if self.old_pos is not None:
            delta = QPoint(event.globalPos() - self.old_pos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPos()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.old_pos = None

    # --- Update Methods ---
    def update_transcript(self, text: str):
        self.transcript_area.setPlainText(text)
        scroll = self.transcript_area.verticalScrollBar()
        scroll.setValue(scroll.maximum())

    def update_suggestion(self, text: str):
        self.suggestion_area.setPlainText(text)
        scroll = self.suggestion_area.verticalScrollBar()
        scroll.setValue(scroll.maximum())

    def update_status(self, status: str):
        if status.lower() == "listening":
            self.status_label.setText("● Listening")
            self.status_label.setStyleSheet("color: #00FFAA; font-weight: bold; font-size: 12px;")
        elif status.lower() == "processing":
            self.status_label.setText("● Processing...")
            self.status_label.setStyleSheet("color: #FFAA00; font-weight: bold; font-size: 12px;")
        else:
            self.status_label.setText(f"● {status}")
            self.status_label.setStyleSheet("color: #AAAAAA; font-weight: bold; font-size: 12px;")
