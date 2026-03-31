from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout, QButtonGroup, QRadioButton
from PySide6.QtCore import Signal
import re
from config.settings import MODEL_GPT, MODEL_LLAMA
from ai.ai_manager import generate_feedback, generate_questions


def parse_questions_text(preguntas_texto, max_preguntas=5):
    preguntas_parseadas = []
    pregunta_actual = None

    for linea in preguntas_texto.splitlines():
        texto = linea.strip()
        if not texto:
            continue

        match_pregunta = re.match(r"^\d+[\)\.\-:]\s*(.+)$", texto)
        if match_pregunta:
            if pregunta_actual:
                preguntas_parseadas.append(pregunta_actual)
            pregunta_actual = {
                "pregunta": match_pregunta.group(1).strip(),
                "opciones": []
            }
            continue

        match_opcion = re.match(r"^([A-Da-d])[\)\.\-:]\s*(.+)$", texto)
        if match_opcion and pregunta_actual:
            pregunta_actual["opciones"].append(match_opcion.group(2).strip())
            continue

        if pregunta_actual:
            if pregunta_actual["opciones"]:
                pregunta_actual["opciones"][-1] = f"{pregunta_actual['opciones'][-1]} {texto}"
            else:
                pregunta_actual["pregunta"] = f"{pregunta_actual['pregunta']} {texto}"

    if pregunta_actual:
        preguntas_parseadas.append(pregunta_actual)

    if not preguntas_parseadas:
        lineas = [linea.strip() for linea in preguntas_texto.splitlines() if linea.strip()]
        for linea in lineas[:max_preguntas]:
            preguntas_parseadas.append({"pregunta": linea, "opciones": []})

    return preguntas_parseadas[:max_preguntas]


class TestPanel(QWidget):
    pregunta_cambiada = Signal(int, int)
    
    def __init__(self):
        super().__init__()
        
        self.modelo_seleccionado = None
        self.texto_pdf = ""
        self.pregunta_actual = 0
        self.total_preguntas = 0
        self.max_preguntas = 5
        self.lista_preguntas = []
        self.respuestas_usuario = {}
        
        layout_main = QVBoxLayout()
        layout_header = QHBoxLayout()
        
        self.button_gpt = QPushButton("Gpt")
        self.button_llama = QPushButton("Llama")
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
        self.test_view.setWordWrap(True)

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
        self.test_feedback.setWordWrap(True)
        
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
        self.button_Gemini.clicked.connect(self.mostrar_modelo_no_disponible)
        self.button_test.clicked.connect(self.iniciar_test)
        self.answer_group.idClicked.connect(self.guardar_respuesta_actual)
    
    def set_modelo(self, modelo):
        if not modelo:
            self.test_feedback.setText("Ese modelo no está configurado en variables de entorno.")
            return

        self.modelo_seleccionado = modelo
        self.test_feedback.setText(f"Modelo seleccionado: {modelo}")

    def mostrar_modelo_no_disponible(self):
        self.test_feedback.setText("Gemini aún no está integrado.")

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
            self.total_preguntas = len(self.lista_preguntas)

            if self.total_preguntas == 0:
                self.test_view.setText("No se pudieron generar preguntas válidas.")
                self.pregunta_actual = 0
                self.pregunta_cambiada.emit(0, 0)
                return

            self.respuestas_usuario = {}
            self.pregunta_actual = 1
            self.mostrar_pregunta_actual()
            self.pregunta_cambiada.emit(self.pregunta_actual, self.total_preguntas)
        except Exception as error:
            self.test_view.setText(f"Error al generar preguntas: {error}")

    def parsear_preguntas(self, preguntas_texto):
        return parse_questions_text(preguntas_texto, max_preguntas=self.max_preguntas)

    def mostrar_pregunta_actual(self):
        if self.pregunta_actual == 0:
            self.test_view.setText("Aún no hay preguntas generadas.")
            self.limpiar_seleccion()
            return

        indice = self.pregunta_actual - 1
        if 0 <= indice < len(self.lista_preguntas):
            pregunta_actual = self.lista_preguntas[indice]
            self.test_view.setText(pregunta_actual.get("pregunta", ""))
            self.actualizar_opciones(pregunta_actual.get("opciones", []))
            self.restaurar_seleccion_actual()
        else:
            self.test_view.setText("No hay más preguntas disponibles.")
            self.actualizar_opciones([])
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

    def actualizar_opciones(self, opciones):
        letras = ["A", "B", "C", "D"]
        for indice, radio in enumerate(self.radio_opciones):
            if indice < len(opciones):
                radio.setText(f"{letras[indice]}) {opciones[indice]}")
                radio.setEnabled(True)
                radio.show()
            else:
                radio.setText(f"{letras[indice]})")
                radio.setEnabled(False)
                radio.show()

    def finalizar_test(self):
        if self.total_preguntas == 0 or not self.lista_preguntas:
            self.test_feedback.setText("Primero inicia un test para poder finalizarlo.")
            return

        if not self.modelo_seleccionado:
            self.test_feedback.setText("Selecciona un modelo para generar retroalimentación.")
            return

        resumen_lineas = []
        letras = ["A", "B", "C", "D"]

        for indice, pregunta in enumerate(self.lista_preguntas, start=1):
            texto_pregunta = pregunta.get("pregunta", "").strip()
            opcion_id = self.respuestas_usuario.get(indice)
            if opcion_id is None:
                respuesta = "Sin responder"
            else:
                opciones = pregunta.get("opciones", [])
                if 0 <= opcion_id < len(opciones):
                    respuesta = f"{letras[opcion_id]}) {opciones[opcion_id]}"
                else:
                    respuesta = "Respuesta inválida"

            resumen_lineas.append(f"Pregunta {indice}: {texto_pregunta}")
            resumen_lineas.append(f"Respuesta: {respuesta}")
            resumen_lineas.append("")

        resumen = "\n".join(resumen_lineas).strip()

        try:
            feedback = generate_feedback(resumen, self.modelo_seleccionado)
            self.test_feedback.setText(feedback)
        except Exception as error:
            self.test_feedback.setText(f"Error al generar retroalimentación: {error}")
        
        