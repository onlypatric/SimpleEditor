
from PyQt6.QtCore import Qt,QRegularExpression
from PyQt6.QtGui import QTextCharFormat, QSyntaxHighlighter,QColor,QTextBlockFormat
from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit
import sys

class SclHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)

        KEYWORD_COLOR = QColor(130,39,214)
        LOCAL_VAR_COLOR = QColor(242, 80, 34)
        TYPE_COLOR = QColor(0,164,239)
        INPUT_VAR_COLOR = QColor(230,0,35)
        OUTPUT_VAR_COLOR = QColor(120,194,87)
        COMMENT_COLOR = QColor("#354f3c")
        STRING_COLOR = QColor(255, 0, 191)
        TYPES = [
            "Int","Bool","UInt","USInt"
        ]

        self.highlighting_rules = [
            (QRegularExpression(r"\bVAR\b|\bVAR_INPUT\b|\bVAR_OUTPUT\b|\bRETAIN\b|\bEND_VAR\b"), KEYWORD_COLOR),  # VAR
            (QRegularExpression(r"\bIF\b|\bTHEN\b|\bELSE\b|\bEND_IF\b|\bNOT\b|\bTHEN\b|\bAND\b|\bOR\b"), KEYWORD_COLOR),  # IF, THEN, ELSE, END_IF
            (QRegularExpression(r"\bCASE\b|\bOF\b|\bEND_CASE\b"), KEYWORD_COLOR),  # CASE, OF, END_CASE
            (QRegularExpression(r"\bFOR\b|\bBEGIN\b|\bREGION\b|\bEND_REGION\b|\bTO\b|\bBY\b|\bDO\b|\bEND_FOR\b|\bFUNCTION_BLOCK\b|\bEND_FUNCTION_BLOCK\b"), KEYWORD_COLOR),  # FOR, TO, BY, DO, END_FOR
            (QRegularExpression(r"|".join([rf"\b{varType}\b" for varType in TYPES])), TYPE_COLOR), # Types
            (QRegularExpression(r'\b(AUX[^\s]+|AUX)\b|\b(#AUX[^\s]+|AUX)\b|\b(Aux[^\s+]+|Aux)\b'),LOCAL_VAR_COLOR), # Aux function block input

            (QRegularExpression(r'\b(IN[^\s]+|IN)\b|\b(#IN[^\s]+|#IN)\b'), INPUT_VAR_COLOR),
            (QRegularExpression(r'\b(OUT[^\s]+|OUT)\b|\b(#OUT[^\s]+|#OUT)\b'), OUTPUT_VAR_COLOR),
            (QRegularExpression(r'//(.*)$'), COMMENT_COLOR),
            (QRegularExpression(r'"([^"]*)"'), STRING_COLOR),

        ]

    def highlightBlock(self, text):
        for pattern, format in self.highlighting_rules:
            expression = QRegularExpression(pattern)
            match = expression.match(text)

            while match.hasMatch():

                start = match.capturedStart()
                length = match.capturedLength()
                self.setFormat(start, length, format)
                match = expression.match(text, start + length)
