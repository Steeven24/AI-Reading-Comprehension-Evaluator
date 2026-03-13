import sys
from PySide6.QtWidgets import QApplication
from ui.main_screen import MainWindow

app = QApplication(sys.argv)

window = MainWindow()
window.show()

sys.exit(app.exec())