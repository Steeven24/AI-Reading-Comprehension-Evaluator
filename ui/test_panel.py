from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QGridLayout, QHBoxLayout
from config.settings import MODEL_GPT, MODEL_LLAMA
from ai.ai_manager import generate_questions

class TestPanel(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.modelo_seleccionado = None
        self.texto_pdf = ""
        
        layout_main = QVBoxLayout()
        layout_header = QHBoxLayout()
        
        self.button_gpt = QPushButton("Gpt")
        self.button_llama = QPushButton("llama")
        self.button_Gemini = QPushButton("Gemini")
        self.button_test = QPushButton("Iniciar Test")
        
        
        self.button_test.setFixedSize(100,40)
        
        layout_main.addLayout(layout_header)
        layout_header.addWidget(self.button_gpt)
        layout_header.addWidget(self.button_llama)
        layout_header.addWidget(self.button_Gemini)
        layout_main.addWidget(self.button_test)
        
        label_test = QLabel("Preguntas de Comprension")
        label_test.setFixedSize(200,30)
        
        self.test_view = QLabel()
        self.test_view.setMinimumSize(400,100)
        self.test_view.setStyleSheet("border: 1px solid black;")
        
        label_feedback = QLabel("Retroalimentacion")
        label_feedback.setFixedSize(200,30)
        
        self.test_feedback = QLabel()
        self.test_feedback.setMinimumSize(400,50)
        self.test_feedback.setStyleSheet("border: 1px solid black;")
        
        layout_main.addWidget(label_test)
        layout_main.addWidget(self.test_view)
        layout_main.addWidget(label_feedback)
        layout_main.addWidget(self.test_feedback)
        
        self.setLayout(layout_main)
        
        #conexiones
        self.button_gpt.clicked.connect(lambda: self.set_modelo(MODEL_GPT))
        self.button_llama.clicked.connect(lambda: self.set_modelo(MODEL_LLAMA))
        self.button_test.clicked.connect(self.iniciar_test)
    
    def seleccionar_modelo(self, modelo):
        self.modelo_seleccionado = modelo
        
        print(f"Modelo seleccionado: {modelo}")

    def set_modelo(self, modelo):
        self.seleccionar_modelo(modelo)

    def set_texto_pdf(self, texto):
        self.texto_pdf = texto

    def iniciar_test(self):
        if not self.texto_pdf.strip():
            self.test_view.setText("Primero sube un PDF en el panel izquierdo.")
            return

        if not self.modelo_seleccionado:
            self.test_view.setText("Primero selecciona un modelo (GPT o Llama).")
            return

        try:
            preguntas = generate_questions(self.texto_pdf, self.modelo_seleccionado)
            self.test_view.setText(preguntas)
        except Exception as error:
            self.test_view.setText(f"Error al generar preguntas: {error}")
        
        