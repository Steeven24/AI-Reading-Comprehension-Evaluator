from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QGridLayout, QHBoxLayout

class TestPanel(QWidget):
    
    def __init__(self):
        super().__init__()
        
        layout_main = QVBoxLayout()
        layout_header = QHBoxLayout()
        
        button_gpt = QPushButton("Gpt")
        button_llama = QPushButton("llama")
        button_Gemini = QPushButton("Gemini")
        button_test = QPushButton("Iniciar Test")
        
        button_test.setFixedSize(100,40)
        
        layout_main.addLayout(layout_header)
        layout_header.addWidget(button_gpt)
        layout_header.addWidget(button_llama)
        layout_header.addWidget(button_Gemini)
        layout_main.addWidget(button_test)
        
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
        
        