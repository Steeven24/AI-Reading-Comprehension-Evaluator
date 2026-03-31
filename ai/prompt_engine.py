from textwrap import dedent

MAX_PROMPT_TEXT_CHARS = 3000


def build_questions_prompt(texto: str) -> str:
    texto_recortado = (texto or "").strip()[:MAX_PROMPT_TEXT_CHARS]
    return dedent(
        f"""
        Actúa como un profesor universitario.

        Lee el siguiente contenido y genera 5 preguntas de comprensión lectora de opción múltiple:

        {texto_recortado}

        Requisitos:
        - Preguntas claras
        - Nivel intermedio
        - Numeradas del 1 al 5
        - Cada pregunta debe tener exactamente 4 opciones: A), B), C), D)
        - No incluyas la respuesta correcta
        - Sin explicaciones

        Formato obligatorio:
        1) [pregunta]
        A) [opción]
        B) [opción]
        C) [opción]
        D) [opción]
        """
    ).strip()


def build_question_feedback_prompt(pregunta: str, respuesta_usuario: str) -> str:
    return dedent(
        f"""
        Actua como tutor de comprension lectora.

        Evalua una sola respuesta del estudiante para esta pregunta:
        Pregunta: {pregunta}
        Respuesta seleccionada: {respuesta_usuario}

        Entrega una retroalimentacion breve y accionable (2 a 4 lineas):
        - Que estuvo bien
        - Que mejorar
        - Una recomendacion concreta
        """
    ).strip()


def build_test_summary_feedback_prompt(preguntas_y_respuestas: str) -> str:
    return dedent(
        f"""
        Actua como docente y genera una retroalimentacion FINAL del test de comprension lectora.

        Respuestas del estudiante por pregunta:
        {preguntas_y_respuestas}

        Requisitos:
        - No repitas ni resuelvas una sola pregunta de forma aislada.
        - Entrega una vision global del desempeno.
        - Incluye fortalezas, debilidades y recomendaciones de estudio.
        - Maximo 8 lineas.
        """
    ).strip()