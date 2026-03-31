from PySide6.QtWidgets import QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QSplitter
from PySide6.QtCore import Qt
from ui.pdf_panel import PdfPanel
from ui.test_panel import TestPanel

class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Test de Comprension Lectora con IA")
        self.setGeometry(100, 100, 1080, 720)

        self.button_next = QPushButton("Siguiente pregunta")
        self.button_next.setEnabled(False)

        splitter = QSplitter(Qt.Horizontal)

        self.panel_pdf = PdfPanel()
        self.panel_test = TestPanel()
        self.panel_pdf.texto_extraido.connect(self.panel_test.set_texto_pdf)

        self.panel_test.pregunta_cambiada.connect(self.actualizar_label_pregunta)
        self.button_next.clicked.connect(self.panel_test.siguiente_pregunta)

        label_numtest = QLabel("Pregunta 0 / 0")
        self.label_numtest = label_numtest

        layout_bottom = QHBoxLayout()
        layout_bottom.addWidget(self.label_numtest)
        layout_bottom.addStretch()
        layout_bottom.addWidget(self.button_next)

        contenedor = QWidget()
        layout_main = QVBoxLayout(contenedor)

        splitter.addWidget(self.panel_pdf)
        splitter.addWidget(self.panel_test)

        layout_main.addWidget(splitter)
        layout_main.addLayout(layout_bottom)

        self.setCentralWidget(contenedor)

    def actualizar_label_pregunta(self, pregunta_actual, total_preguntas):
        self.label_numtest.setText(f"Pregunta {pregunta_actual} / {total_preguntas}")
        self.button_next.setEnabled(total_preguntas > 0 and pregunta_actual < total_preguntas)
        
        
        
        
        
        
