from PyQt5.QtWidgets import (
    QMainWindow, QPlainTextEdit, QSplitter, QWidget,
    QVBoxLayout, QFileDialog, QMessageBox
)
from ir_model import IRModel
from ir_highlighter import IRHighlighter
from symbol_view import SymbolView

class IRViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LLVM IR Viewer")
        self.resize(1000, 700)

        self.model = IRModel()
        self.sym_view = SymbolView()
        self.editor = QPlainTextEdit()
        self.editor.setReadOnly(True)
        IRHighlighter(self.editor.document())

        splitter = QSplitter()
        splitter.addWidget(self.sym_view)
        splitter.addWidget(self.editor)
        splitter.setStretchFactor(1, 4)

        container = QWidget()
        layout = QVBoxLayout(container)
        layout.addWidget(splitter)
        self.setCentralWidget(container)

        self.sym_view.itemClicked.connect(self.on_symbol_click)
        self._create_menu()

    def _create_menu(self):
        m = self.menuBar().addMenu("File")
        open_act = m.addAction("Open IR…")
        open_act.triggered.connect(self.open_ir)

    def open_ir(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open LLVM IR", "", "IR files (*.ll *.llvm)")
        if not path:
            return

        try:
            self.model.load_ir(path)
        except Exception as e:
            QMessageBox.warning(self, "Error loading IR", str(e))
            return

        self.editor.setPlainText(self.model.text())
        self.sym_view.load_symbols(self.model.symbols())

    def on_symbol_click(self, item, _col):
        line_no = item.data(0, 1)
        if line_no is None:
            return
        cursor = self.editor.textCursor()
        block = self.editor.document().findBlockByNumber(line_no)
        cursor.setPosition(block.position())
        self.editor.setTextCursor(cursor)
        self.editor.setFocus()