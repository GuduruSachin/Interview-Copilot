from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, QHBoxLayout, QDesktopWidget
from PyQt5.QtCore import Qt, QPoint
from utils.logger import get_logger

logger = get_logger(__name__)

class OverlayWindow(QWidget):
    def __init__(self, stop_callback=None):
        super().__init__()
        self.stop_callback = stop_callback
        self.old_pos = None
        self.resize_mode = 0
        self.is_expanded = False
        self.setup_ui()
        self.setMouseTracking(True)

    def setup_ui(self):
        # Mandatory Window Properties
        self.setWindowFlags(
            Qt.FramelessWindowHint | 
            Qt.WindowStaysOnTopHint | 
            Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        self.setWindowOpacity(0.85)

        # Default size and positioning
        self.setMinimumSize(500, 300)
        self.resize(700, 450)
        self._position_bottom_right()

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(10)

        # Top Bar: Status and Actions
        top_bar_layout = QHBoxLayout()
        
        self.status_label = QLabel("● Listening")
        self.status_label.setStyleSheet("color: #00FFAA; font-weight: bold; font-size: 13px;")
        
        self.expand_btn = QPushButton("⬜")
        self.expand_btn.setFixedSize(26, 26)
        self.expand_btn.setToolTip("Toggle Size")
        self.expand_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 20);
                color: #FFFFFF;
                border-radius: 4px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: rgba(255, 255, 255, 40); }
        """)
        self.expand_btn.clicked.connect(self.toggle_expand)

        self.stop_btn = QPushButton("Stop")
        self.stop_btn.setFixedSize(60, 26)
        self.stop_btn.setStyleSheet("""
            QPushButton {
                background-color: #ff4444;
                color: white;
                border-radius: 4px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #ff6666; }
        """)
        if self.stop_callback:
            self.stop_btn.clicked.connect(self.stop_callback)

        top_bar_layout.addWidget(self.status_label)
        top_bar_layout.addStretch()
        top_bar_layout.addWidget(self.expand_btn)
        top_bar_layout.addWidget(self.stop_btn)

        # Content Area (Transcript and Suggestion side by side)
        content_layout = QHBoxLayout()
        content_layout.setSpacing(12)

        # LEFT: Transcript
        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(0, 0, 0, 0)
        transcript_label = QLabel("Transcript")
        transcript_label.setStyleSheet("color: #AAAAAA; font-size: 12px; font-weight: bold;")
        
        self.transcript_area = QTextEdit()
        self.transcript_area.setReadOnly(True)
        self.transcript_area.setLineWrapMode(QTextEdit.WidgetWidth)
        self.transcript_area.setStyleSheet("""
            QTextEdit {
                background-color: rgba(0, 0, 0, 100);
                color: white;
                border: 1px solid rgba(255, 255, 255, 30);
                border-radius: 8px;
                padding: 10px;
                font-size: 15px;
                line-height: 1.5;
            }
        """)
        left_layout.addWidget(transcript_label)
        left_layout.addWidget(self.transcript_area)

        # RIGHT: AI Suggestion
        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(0, 0, 0, 0)
        suggestion_label = QLabel("Suggestion")
        suggestion_label.setStyleSheet("color: #AAAAAA; font-size: 12px; font-weight: bold;")
        
        self.suggestion_area = QTextEdit()
        self.suggestion_area.setReadOnly(True)
        self.suggestion_area.setLineWrapMode(QTextEdit.WidgetWidth)
        self.suggestion_area.setStyleSheet("""
            QTextEdit {
                background-color: rgba(0, 0, 0, 100);
                color: white;
                border: 1px solid rgba(255, 255, 255, 30);
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
                line-height: 1.5;
            }
        """)
        right_layout.addWidget(suggestion_label)
        right_layout.addWidget(self.suggestion_area)

        # Add left and right sections with correct stretch
        content_layout.addLayout(left_layout, 2)
        content_layout.addLayout(right_layout, 1)

        # Add elements to main layout
        main_layout.addLayout(top_bar_layout)
        main_layout.addLayout(content_layout)

        self.setLayout(main_layout)

        # Apply global style to overlay background
        self.setStyleSheet("""
            OverlayWindow {
                background-color: rgba(20, 20, 20, 180);
                border-radius: 12px;
            }
        """)

    def _position_bottom_right(self):
        screen = QDesktopWidget().availableGeometry()
        width = 700
        height = 450
        x = screen.width() - width - 40
        y = screen.height() - height - 40
        self.move(x, y)

    def toggle_expand(self):
        if self.is_expanded:
            self.resize(700, 450)
            self.is_expanded = False
        else:
            self.resize(1000, 700)
            self.is_expanded = True
    
    # --- Draggable & Resizable Window Methods ---
    def _get_resize_mode(self, pos):
        margin = 15
        mode = 0
        if pos.x() < margin:
            mode |= 1 # left
        elif pos.x() > self.width() - margin:
            mode |= 2 # right
        if pos.y() < margin:
            mode |= 4 # top
        elif pos.y() > self.height() - margin:
            mode |= 8 # bottom
        return mode

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.old_pos = event.globalPos()
            self.resize_mode = self._get_resize_mode(event.pos())

    def mouseMoveEvent(self, event):
        if getattr(self, 'old_pos', None) is not None:
            delta = event.globalPos() - self.old_pos
            if self.resize_mode == 0:
                # Move
                self.move(self.x() + delta.x(), self.y() + delta.y())
                self.old_pos = event.globalPos()
            else:
                # Resize
                rect = self.geometry()
                if self.resize_mode & 1: # left
                    rect.setLeft(rect.left() + delta.x())
                if self.resize_mode & 2: # right
                    rect.setRight(rect.right() + delta.x())
                if self.resize_mode & 4: # top
                    rect.setTop(rect.top() + delta.y())
                if self.resize_mode & 8: # bottom
                    rect.setBottom(rect.bottom() + delta.y())
                
                # Check min size to prevent shrinking too small
                if rect.width() >= self.minimumWidth() and rect.height() >= self.minimumHeight():
                    self.setGeometry(rect)
                    self.old_pos = event.globalPos()
        else:
            # Update cursor if hovering over edges
            mode = self._get_resize_mode(event.pos())
            if mode in (1, 2):
                self.setCursor(Qt.SizeHorCursor)
            elif mode in (4, 8):
                self.setCursor(Qt.SizeVerCursor)
            elif mode in (5, 10):
                self.setCursor(Qt.SizeFDiagCursor)
            elif mode in (6, 9):
                self.setCursor(Qt.SizeBDiagCursor)
            else:
                self.setCursor(Qt.ArrowCursor)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.old_pos = None
            self.resize_mode = 0

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
            self.status_label.setStyleSheet("color: #00FFAA; font-weight: bold; font-size: 13px;")
        elif status.lower() == "processing":
            self.status_label.setText("● Processing...")
            self.status_label.setStyleSheet("color: #FFAA00; font-weight: bold; font-size: 13px;")
        else:
            self.status_label.setText(f"● {status}")
            self.status_label.setStyleSheet("color: #AAAAAA; font-weight: bold; font-size: 13px;")
