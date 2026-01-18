import sys
from PyQt6.QtWidgets import QApplication
from ui import PNGApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PNGApp()
    window.show()
    sys.exit(app.exec())