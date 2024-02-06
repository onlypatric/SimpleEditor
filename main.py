import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import *

APP_DETAILS = {
    "title": "SCL editor",
    "author": "Patric Pintescul",
    "version": "1.0",
}

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(APP_DETAILS["title"])
        self.setContentsMargins(0,0,0,0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())