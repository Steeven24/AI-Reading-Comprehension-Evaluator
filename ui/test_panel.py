from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout, QButtonGroup, QRadioButton
from PySide6.QtCore import Signal
from config.settings import MODEL_GPT, MODEL_LLAMA
from ai.ai_manager import generate_questions

class TestPanel(QWidget):
    pregunta_cambiada = Signal(int, int)
    
    def __init__(self):
        super().__init__()
        
        self.modelo_seleccionado = None
        self.texto_pdf = ""
        self.pregunta_actual = 0
        self.total_preguntas = 5
        self.lista_preguntas = []
        self.respuestas_usuario = {}
        
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

        self.answer_group = QButtonGroup(self)
        self.answer_group.setExclusive(True)
        self.radio_opciones = []

        for indice, letra in enumerate(["A", "B", "C", "D"]):
            radio = QRadioButton(f"Opción {letra}")
            self.answer_group.addButton(radio, indice)
            self.radio_opciones.append(radio)
        
        label_feedback = QLabel("Retroalimentacion")
        label_feedback.setFixedSize(200,30)
        
        self.test_feedback = QLabel()
        self.test_feedback.setMinimumSize(400,50)
        self.test_feedback.setStyleSheet("border: 1px solid black;")
        
        layout_main.addWidget(label_test)
        layout_main.addWidget(self.test_view)
        for radio in self.radio_opciones:
            layout_main.addWidget(radio)
        layout_main.addWidget(label_feedback)
        layout_main.addWidget(self.test_feedback)
        
        self.setLayout(layout_main)
        
        #conexiones
        self.button_gpt.clicked.connect(lambda: self.set_modelo(MODEL_GPT))
        self.button_llama.clicked.connect(lambda: self.set_modelo(MODEL_LLAMA))
        self.button_test.clicked.connect(self.iniciar_test)
        self.answer_group.idClicked.connect(self.guardar_respuesta_actual)
    
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
            self.lista_preguntas = self.parsear_preguntas(preguntas)
            self.respuestas_usuario = {}
            self.pregunta_actual = 1
            self.mostrar_pregunta_actual()
            self.pregunta_cambiada.emit(self.pregunta_actual, self.total_preguntas)
        except Exception as error:
            self.test_view.setText(f"Error al generar preguntas: {error}")

    def parsear_preguntas(self, preguntas_texto):
        preguntas = [linea.strip() for linea in preguntas_texto.splitlines() if linea.strip()]
        return preguntas[:self.total_preguntas]

    def mostrar_pregunta_actual(self):
        if self.pregunta_actual == 0:
            self.test_view.setText("Aún no hay preguntas generadas.")
            self.limpiar_seleccion()
            return

        indice = self.pregunta_actual - 1
        if 0 <= indice < len(self.lista_preguntas):
            self.test_view.setText(self.lista_preguntas[indice])
            self.restaurar_seleccion_actual()
        else:
            self.test_view.setText("No hay más preguntas disponibles.")
            self.limpiar_seleccion()

    def siguiente_pregunta(self):
        if self.pregunta_actual == 0:
            return

        if self.pregunta_actual < self.total_preguntas:
            self.pregunta_actual += 1

        self.mostrar_pregunta_actual()
        self.pregunta_cambiada.emit(self.pregunta_actual, self.total_preguntas)

    def guardar_respuesta_actual(self, opcion_id):
        if self.pregunta_actual == 0:
            return

        self.respuestas_usuario[self.pregunta_actual] = opcion_id

    def limpiar_seleccion(self):
        self.answer_group.setExclusive(False)
        for radio in self.radio_opciones:
            radio.setChecked(False)
        self.answer_group.setExclusive(True)

    def restaurar_seleccion_actual(self):
        self.limpiar_seleccion()
        opcion_guardada = self.respuestas_usuario.get(self.pregunta_actual)
        if opcion_guardada is None:
            return

        if 0 <= opcion_guardada < len(self.radio_opciones):
            self.radio_opciones[opcion_guardada].setChecked(True)
        
        