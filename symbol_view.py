from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem

class SymbolView(QTreeWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setHeaderHidden(True)

    def load_symbols(self, symbols: dict):
        self.clear()
        for category, items in symbols.items():
            cat_item = QTreeWidgetItem([category])
            for name, line_no in items:
                entry = QTreeWidgetItem([name])
                entry.setData(0, 1, line_no)
                cat_item.addChild(entry)
            self.addTopLevelItem(cat_item)
        self.expandAll()