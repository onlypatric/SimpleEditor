import sys
from PyQt6.QtCore import Qt,QSettings,QPoint
from PyQt6.QtGui import QKeySequence, QIcon, QPixmap, QTextOption
from PyQt6.QtWidgets import *

APP_DETAILS = {
    "title": "SCL editor",
    "author": "Patric Pintescul",
    "version": "1.0",
    "app-name": "scl-editor",
}

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("main-window")

        self.settings = QSettings("Pintescul Patric", APP_DETAILS["app-name"])

        self.restoreGeometry(self.settings.value("geometry", self.saveGeometry()))

        self.setWindowTitle(APP_DETAILS["title"])
        self.setContentsMargins(0,0,0,0)

        self.setCentralWidget(CentralWidget(self))
    def closeEvent(self, close_event) -> None:
        self.settings.setValue("geometry", self.saveGeometry())
        super().closeEvent(close_event)

class CentralWidget(QWidget):
    def __init__(self, parent: MainWindow | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("central-widget")
        self.setContentsMargins(0,0,0,0)

        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.text_edit = TextEdit(self)

        self.main_layout.addWidget(self.text_edit)
        self.setLayout(self.main_layout)

class TextEdit(QPlainTextEdit):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("text-edit")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)  # Set size policy to expanding

        self.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        self.setWordWrapMode(QTextOption.WrapMode.NoWrap)
        self.setTabStopDistance(20)
        self.setTabChangesFocus(True)
        self.setUndoRedoEnabled(False)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.on_context_menu)

    def on_context_menu(self, pos: QPoint) -> None:
        menu = QMenu()

        # Load SVG icon for "Copy" action
        copy_icon = QIcon()
        copy_icon.addPixmap(QPixmap("path/to/copy.svg"), QIcon.Mode.Normal, QIcon.State.Off)
        
        # Create actions with icons and shortcuts
        copy_action = QAction(copy_icon, "Copy", self)
        copy_action.setShortcut(QKeySequence.Copy)

        paste_action = QAction("Paste", self)
        paste_action.setShortcut(QKeySequence.Paste)

        cut_action = QAction("Cut", self)
        cut_action.setShortcut(QKeySequence.Cut)

        select_all_action = QAction("Select All", self)
        select_all_action.setShortcut(QKeySequence.SelectAll)

        # Add actions to the menu
        menu.addAction(copy_action)
        menu.addAction(paste_action)
        menu.addAction(cut_action)
        menu.addAction(select_all_action)

        # Execute the menu at the specified position
        menu.exec(self.mapToGlobal(pos))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())