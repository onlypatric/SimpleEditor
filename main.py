import re
import sys
from PyQt6.QtCore import Qt,QSettings,QPoint,QEvent,QStringListModel
from PyQt6.QtGui import QKeySequence, QIcon, QPixmap, QTextOption, QAction,QColor,QTextCharFormat,QFont,QTextCursor
from PyQt6.QtWidgets import *
from highlighter import SclHighlighter

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

        self.menu = self.menuBar()
        # File menu
        self.file_menu = self.menu.addMenu("File")

        # Edit menu
        self.edit_menu = self.menu.addMenu("Edit")
        
        self.setCentralWidget(CentralWidget(self))



    def closeEvent(self, close_event) -> None:
        self.settings.setValue("geometry", self.saveGeometry())
        super().closeEvent(close_event)

class CentralWidget(QWidget):
    def __init__(self, parent: MainWindow | None = None) -> None:
        super().__init__(parent)
        self.p=parent
        self.setObjectName("central-widget")
        self.setContentsMargins(0,0,0,0)

        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.text_edit = TextEdit(self)

        self.main_layout.addWidget(self.text_edit)
        self.setLayout(self.main_layout)


class TextEdit(QPlainTextEdit):
    def __init__(self, parent: CentralWidget | None = None) -> None:
        super().__init__(parent)
        self.p = parent
        self.highlighter = SclHighlighter(self.document())

        self.setTabStopDistance(20)
        self.setFont(QFont("JetBrainsMono Nerd Font",18))

        self.setObjectName("text-edit")
        self.setSizePolicy(QSizePolicy.Policy.Expanding,
                           QSizePolicy.Policy.Expanding)

        self.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        self.setWordWrapMode(QTextOption.WrapMode.NoWrap)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.on_context_menu)

        self.undo_action = QAction("Undo", self)
        self.undo_action.setShortcut(QKeySequence.StandardKey.Undo)
        self.undo_action.triggered.connect(self.undo)

        self.redo_action = QAction("Redo", self)
        self.redo_action.setShortcut(QKeySequence.StandardKey.Redo)
        self.redo_action.triggered.connect(self.redo)

        # Create actions for copy, paste, cut, and select all
        self.copy_action = QAction("Copy", self)
        self.copy_action.setShortcut(QKeySequence.StandardKey.Copy)
        self.copy_action.triggered.connect(self.copy)

        self.paste_action = QAction("Paste", self)
        self.paste_action.setShortcut(QKeySequence.StandardKey.Paste)
        self.paste_action.triggered.connect(self.paste)

        self.cut_action = QAction("Cut", self)
        self.cut_action.setShortcut(QKeySequence.StandardKey.Cut)
        self.cut_action.triggered.connect(self.cut)

        self.select_all_action = QAction("Select All", self)
        self.select_all_action.setShortcut(QKeySequence.StandardKey.SelectAll)
        self.select_all_action.triggered.connect(self.selectAll)

        file_menu = self.p.p.edit_menu

        # icons
        self.undo_action.setIcon(QIcon("assets/undo.svg"))
        self.redo_action.setIcon(QIcon("assets/redo.svg"))
        self.copy_action.setIcon(QIcon("assets/copy.svg"))
        self.paste_action.setIcon(QIcon("assets/paste.svg"))
        self.cut_action.setIcon(QIcon("assets/cut.svg"))

        # Create context menu and add actions
        self.context_menu = QMenu(self)

        self.context_menu.addAction(self.undo_action)
        self.context_menu.addAction(self.redo_action)
        self.context_menu.addSeparator()
        self.context_menu.addAction(self.copy_action)
        self.context_menu.addAction(self.paste_action)
        self.context_menu.addAction(self.cut_action)
        self.context_menu.addSeparator()
        self.context_menu.addAction(self.select_all_action)

        file_menu.addAction(self.undo_action)
        file_menu.addAction(self.redo_action)
        file_menu.addSeparator()
        file_menu.addAction(self.copy_action)
        file_menu.addAction(self.paste_action)
        file_menu.addAction(self.cut_action)
        file_menu.addSeparator()
        file_menu.addAction(self.select_all_action)

        self.keywords = ["IF", "ELSE", "THEN", "END_IF", "FOR", "TO", "DO", "END_FOR", "VAR", "RETAIN", "AUX", "FUNCTION", "CASE", "OF", "END_CASE",
                         "REGION","END_REGION","AND","OR","VAR_END","VAR_INPUT","VAR_OUTPUT","IN"
                         ]

        self.completer = QCompleter(self.keywords, self)
        self.completer.setCompletionMode(QCompleter.CompletionMode.InlineCompletion)
        self.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)

        self.setCompleter(self.completer)

    def setCompleter(self, completer):
        self.completer = completer
        self.completer.setWidget(self)
        self.completer.setCompletionMode(
            QCompleter.CompletionMode.PopupCompletion)
        self.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.completer.activated.connect(self.insertCompletion)

    def insertCompletion(self, completion):
        if self.completer.widget() != self:
            return

        tc = self.textCursor()
        extra = len(completion) - len(self.completer.completionPrefix())
        tc.movePosition(QTextCursor.MoveOperation.Left)
        tc.movePosition(QTextCursor.MoveOperation.Right,
                        QTextCursor.MoveMode.KeepAnchor, extra)
        tc.insertText(completion)
        self.setTextCursor(tc)

    def textUnderCursor(self):
        tc = self.textCursor()
        tc.select(QTextCursor.SelectionType.WordUnderCursor)
        return tc.selectedText()

    def on_context_menu(self, pos):
        self.context_menu.exec(self.mapToGlobal(pos))

    def keyPressEvent(self, event:QEvent):
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            self.updateVariableDisplay()
        cursor = self.textCursor()
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            cursor = self.textCursor()
            block = cursor.block()
            text = block.text()

            # Count the number of leading tabs or spaces
            num_tabs = 0
            for char in text:
                if char == '\t':
                    num_tabs += 1

            # Insert the corresponding number of tabs in the new line
            cursor.insertText('\n' + '\t' * num_tabs)
            self.setTextCursor(cursor)
            return
        elif event.text() == "(":
            super().keyPressEvent(event)
            cursor.insertText(")")
            cursor.movePosition(QTextCursor.MoveOperation.Left,
                                QTextCursor.MoveMode.MoveAnchor)
            return
        elif event.text() == "[":
            super().keyPressEvent(event)
            cursor.insertText("]")
            cursor.movePosition(QTextCursor.MoveOperation.Left,
                                QTextCursor.MoveMode.MoveAnchor)
            return
        elif event.text() == "{":
            super().keyPressEvent(event)
            cursor.insertText("}")
            cursor.movePosition(QTextCursor.MoveOperation.Left,
                                QTextCursor.MoveMode.MoveAnchor)
            return
        elif event.text() == "\"":
            super().keyPressEvent(event)
            cursor.insertText("\"")
            cursor.movePosition(QTextCursor.MoveOperation.Left,
                                QTextCursor.MoveMode.MoveAnchor)
            return

        if self.completer.popup().isVisible():
            if event.key() in (Qt.Key.Key_Enter, Qt.Key.Key_Return, Qt.Key.Key_Escape, Qt.Key.Key_Tab, Qt.Key.Key_Backtab):
                event.ignore()
                return

        isShortcut = (event.modifiers(
        ) == Qt.KeyboardModifier.ControlModifier and event.key() == Qt.Key.Key_Space)
        if not self.completer or not isShortcut:
            super().keyPressEvent(event)

        tc = self.textCursor()
        tc.movePosition(QTextCursor.MoveOperation.Left, QTextCursor.MoveMode.KeepAnchor, len(
            self.completer.completionPrefix()))

        self.completer.setCompletionPrefix(self.textUnderCursor())
        popup = self.completer.popup()

        if len(self.completer.completionPrefix()) < 1:
            popup.hide()
            return

        popup.setCurrentIndex(self.completer.completionModel().index(0, 0))

        cr = self.cursorRect()
        cr.setWidth(self.completer.popup().sizeHintForColumn(
            0) + self.completer.popup().verticalScrollBar().sizeHint().width())
        self.completer.complete(cr)

    def extractVariables(self, text):
        # Define regular expressions for VAR_INPUT and VAR_OUTPUT sections
        var_input_pattern = re.compile(
            r'\bVAR_INPUT\b(.*?)\bEND_VAR\b', re.DOTALL)
        var_output_pattern = re.compile(
            r'\bVAR_OUTPUT\b(.*?)\bEND_VAR\b', re.DOTALL)

        # Extract variables from VAR_INPUT section
        var_input_matches = var_input_pattern.findall(text)
        var_input_variables = re.findall(
            r'\b(\w+)\s*:', ''.join(var_input_matches))

        # Extract variables from VAR_OUTPUT section
        var_output_matches = var_output_pattern.findall(text)
        var_output_variables = re.findall(
            r'\b(\w+)\s*:', ''.join(var_output_matches))
        
        return var_input_variables, var_output_variables

    def updateVariableDisplay(self):
        text = self.toPlainText()
        var_input, var_output = self.extractVariables(text)
        # Update the display with the extracted variables (implement this part)
        orig_list = self.completer.model()
        new_list = orig_list.stringList() + var_input + var_output
        self.completer.setModel(QStringListModel(new_list))
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("assets/logo.png"))
    app.setStyle("Plastique")
    app.setPalette(app.style().standardPalette())
    window = MainWindow()
    window.show()
    sys.exit(app.exec())