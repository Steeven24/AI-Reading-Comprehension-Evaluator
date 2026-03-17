def build_questions_prompt(texto):
    return f"""
    Actúa como un profesor universitario.

    Lee el siguiente contenido y genera 3 preguntas de comprensión:

    {texto}

    Requisitos:
    - Preguntas claras
    - Nivel intermedio
    - Numeradas
    - Sin explicaciones
    """


def build_feedback_prompt(pregunta, respuesta_usuario):
    return f"""
    Evalúa la siguiente respuesta:

    Pregunta: {pregunta}
    Respuesta del estudiante: {respuesta_usuario}

    Proporciona retroalimentación breve y clara.
    """