def build_questions_prompt(texto):
    return f"""
    Actúa como un profesor universitario.

    Lee el siguiente contenido y genera 5 preguntas de comprensión de opción múltiple:

    {texto}

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


def build_feedback_prompt(pregunta, respuesta_usuario):
    return f"""
    Evalúa la siguiente respuesta:

    Pregunta: {pregunta}
    Respuesta del estudiante: {respuesta_usuario}

    Proporciona retroalimentación breve y clara.
    """