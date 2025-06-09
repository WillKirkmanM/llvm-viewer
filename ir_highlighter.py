from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
from PyQt5.QtCore import QRegExp

class IRHighlighter(QSyntaxHighlighter):
    KEYWORDS = [
        'define', 'declare', 'global', 'private', 'internal',
        'external', 'constant', 'void', 'float', 'double',
        'label', 'metadata', 'align', r'i[0-9]+'
    ]

    def __init__(self, parent):
        super().__init__(parent)
        self._formats = []

        kw_fmt = QTextCharFormat()
        kw_fmt.setForeground(QColor('blue'))
        kw_fmt.setFontWeight(QFont.Bold)
        for kw in self.KEYWORDS:
            rx = QRegExp(r'\b' + kw + r'\b')
            self._formats.append((rx, kw_fmt))

        cm_fmt = QTextCharFormat()
        cm_fmt.setForeground(QColor('green'))
        rx = QRegExp(r';[^\n]*')
        self._formats.append((rx, cm_fmt))

    def highlightBlock(self, text):
        for pattern, fmt in self._formats:
            i = pattern.indexIn(text)
            while i >= 0:
                length = pattern.matchedLength()
                self.setFormat(i, length, fmt)
                i = pattern.indexIn(text, i + length)