import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFont
from ui.main_screen import MainWindow


APP_STYLE = """
QWidget {
	background-color: #f6f8fb;
	color: #1f2937;
	font-family: "Segoe UI", "Tahoma", sans-serif;
	font-size: 12px;
}

QMainWindow {
	background-color: #f3f6fb;
}

QSplitter::handle {
	background-color: #d8dee9;
	width: 2px;
}

QPushButton {
	background-color: #ffffff;
	border: 1px solid #d1d9e6;
	border-radius: 10px;
	padding: 8px 14px;
	color: #1f2937;
	font-weight: 600;
}

QPushButton:hover {
	background-color: #eef3ff;
	border-color: #93b4ff;
}

QPushButton:pressed {
	background-color: #dae7ff;
}

QPushButton:checked {
	background-color: #2f6fdf;
	color: #ffffff;
	border-color: #2a5fbe;
}

QPushButton:disabled {
	background-color: #edf1f7;
	color: #9aa7bd;
	border-color: #dbe2ee;
}

QLabel#SectionTitle {
	font-size: 15px;
	font-weight: 700;
	color: #0f172a;
	margin-top: 6px;
	margin-bottom: 4px;
}

QLabel#StatusLabel {
	color: #334155;
	font-weight: 600;
}

QLabel#PdfCanvas {
	background-color: #ffffff;
	border: 1px solid #d5dbe7;
	border-radius: 14px;
}

QTextEdit {
	background-color: #ffffff;
	border: 1px solid #d5dbe7;
	border-radius: 12px;
	padding: 8px;
	selection-background-color: #cde0ff;
}

QRadioButton {
	spacing: 8px;
	padding: 2px 0;
	color: #1f2937;
}

QRadioButton::indicator {
	width: 16px;
	height: 16px;
}

QRadioButton::indicator:unchecked {
	border: 1px solid #9eb2d9;
	border-radius: 8px;
	background-color: #ffffff;
}

QRadioButton::indicator:checked {
	border: 1px solid #2f6fdf;
	border-radius: 8px;
	background-color: #2f6fdf;
}
"""


def main() -> int:
	app = QApplication(sys.argv)
	app.setFont(QFont("Segoe UI", 10))
	app.setStyleSheet(APP_STYLE)

	window = MainWindow()
	window.show()

	return app.exec()


if __name__ == "__main__":
	sys.exit(main())