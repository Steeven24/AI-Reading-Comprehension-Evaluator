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
        self.button_finish = QPushButton("Finalizar test")
        self.button_finish.setEnabled(False)
        self.button_next.setMinimumHeight(38)
        self.button_finish.setMinimumHeight(38)

        splitter = QSplitter(Qt.Horizontal)
        splitter.setHandleWidth(2)

        self.panel_pdf = PdfPanel()
        self.panel_test = TestPanel()
        self.panel_pdf.texto_extraido.connect(self.panel_test.set_texto_pdf)

        self.panel_test.pregunta_cambiada.connect(self.actualizar_label_pregunta)
        self.button_next.clicked.connect(self.panel_test.siguiente_pregunta)
        self.button_finish.clicked.connect(self.panel_test.finalizar_test)

        label_numtest = QLabel("Pregunta 0 / 0")
        label_numtest.setObjectName("StatusLabel")
        self.label_numtest = label_numtest

        layout_bottom = QHBoxLayout()
        layout_bottom.setContentsMargins(8, 2, 8, 8)
        layout_bottom.setSpacing(10)
        layout_bottom.addWidget(self.label_numtest)
        layout_bottom.addStretch()
        layout_bottom.addWidget(self.button_next)
        layout_bottom.addWidget(self.button_finish)

        contenedor = QWidget()
        layout_main = QVBoxLayout(contenedor)
        layout_main.setContentsMargins(10, 10, 10, 8)
        layout_main.setSpacing(8)

        splitter.addWidget(self.panel_pdf)
        splitter.addWidget(self.panel_test)

        layout_main.addWidget(splitter)
        layout_main.addLayout(layout_bottom)

        self.setCentralWidget(contenedor)

    def actualizar_label_pregunta(self, pregunta_actual, total_preguntas):
        self.label_numtest.setText(f"Pregunta {pregunta_actual} / {total_preguntas}")
        self.button_next.setEnabled(total_preguntas > 0 and pregunta_actual < total_preguntas)
        respuestas_completas = len(self.panel_test.respuestas_usuario) >= total_preguntas and total_preguntas > 0
        en_ultima_pregunta = total_preguntas > 0 and pregunta_actual == total_preguntas
        self.button_finish.setEnabled(en_ultima_pregunta and respuestas_completas)
        
        
        
        
        
        
