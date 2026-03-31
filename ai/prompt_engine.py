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


def build_feedback_prompt(pregunta: str, respuesta_usuario: str) -> str:
    return dedent(
        f"""
        Evalúa la siguiente respuesta:

        Pregunta: {pregunta}
        Respuesta del estudiante: {respuesta_usuario}

        Proporciona retroalimentación breve y clara.
        """
    ).strip()