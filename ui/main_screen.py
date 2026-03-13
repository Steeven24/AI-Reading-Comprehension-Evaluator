from PySide6.QtWidgets import QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QGridLayout, QSplitter
from PySide6.QtCore import Qt
from ui.pdf_panel import PdfPanel

class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Test de Comprension Lectora con IA")
        self.setGeometry(100, 100, 1080, 720)
        
        splitter = QSplitter(Qt.Horizontal)
        
        panel_pdf = PdfPanel()
        
        splitter.addWidget(panel_pdf)
        
        self.setCentralWidget(splitter)
        
        
        
        
        
