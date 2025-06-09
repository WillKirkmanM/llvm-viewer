import sys
from PyQt5.QtWidgets import QApplication
from viewer import IRViewer

def main():
    app = QApplication(sys.argv)
    win = IRViewer()
    win.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()