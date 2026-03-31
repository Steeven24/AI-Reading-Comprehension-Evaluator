from groq import Groq
from config.settings import GEMINI_API_KEY, GROQ_API_KEY
from .prompt_engine import (
    build_question_feedback_prompt,
    build_questions_prompt,
    build_test_summary_feedback_prompt,
)

try:
    from google import genai
except ImportError:
    genai = None


def _is_gemini_model(modelo: str) -> bool:
    return (modelo or "").strip().lower().startswith("gemini")


def _generate_with_gemini(prompt: str, modelo: str) -> str:
    if not GEMINI_API_KEY:
        raise ValueError("Falta GEMINI_API_KEY. Configúrala como variable de entorno.")
    if genai is None:
        raise RuntimeError(
            "Falta el paquete google-genai. Instálalo para usar Gemini."
        )

    client = genai.Client(api_key=GEMINI_API_KEY)
    response = client.models.generate_content(model=modelo, contents=prompt)
    contenido = (getattr(response, "text", "") or "").strip()
    if not contenido:
        raise RuntimeError("Gemini devolvió una respuesta vacía.")
    return contenido

def generate_questions(texto: str, modelo: str) -> str:
    if not modelo:
        raise ValueError("No se recibió un modelo válido para generar preguntas.")

    texto_limpio = (texto or "").strip()
    if not texto_limpio:
        raise ValueError("No hay texto para generar preguntas.")

    prompt = build_questions_prompt(texto_limpio)

    if _is_gemini_model(modelo):
        return _generate_with_gemini(prompt, modelo)

    if not GROQ_API_KEY:
        raise ValueError("Falta GROQ_API_KEY. Configúrala como variable de entorno.")

    client = Groq(api_key=GROQ_API_KEY)

    completion = client.chat.completions.create(
        model=modelo,
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_completion_tokens=500
    )

    contenido = completion.choices[0].message.content
    if not contenido:
        raise RuntimeError("El modelo devolvió una respuesta vacía.")

    return contenido


def _generate_from_prompt(prompt: str, modelo: str, temperature: float, max_tokens: int) -> str:
    if not modelo:
        raise ValueError("No se recibió un modelo válido para generar retroalimentación.")

    if _is_gemini_model(modelo):
        return _generate_with_gemini(prompt, modelo)

    if not GROQ_API_KEY:
        raise ValueError("Falta GROQ_API_KEY. Configúrala como variable de entorno.")

    client = Groq(api_key=GROQ_API_KEY)

    completion = client.chat.completions.create(
        model=modelo,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        max_completion_tokens=max_tokens,
    )

    feedback = completion.choices[0].message.content
    if not feedback:
        raise RuntimeError("El modelo devolvió una retroalimentación vacía.")

    return feedback


def generate_question_feedback(pregunta: str, respuesta_usuario: str, modelo: str) -> str:
    pregunta_limpia = (pregunta or "").strip()
    respuesta_limpia = (respuesta_usuario or "").strip()
    if not pregunta_limpia or not respuesta_limpia:
        raise ValueError("Pregunta y respuesta son obligatorias para generar retroalimentación.")

    prompt = build_question_feedback_prompt(pregunta_limpia, respuesta_limpia)
    return _generate_from_prompt(prompt, modelo, temperature=0.3, max_tokens=240)


def generate_test_feedback(preguntas_y_respuestas: str, modelo: str) -> str:
    contenido = (preguntas_y_respuestas or "").strip()
    if not contenido:
        raise ValueError("No hay respuestas para generar retroalimentación final.")

    prompt = build_test_summary_feedback_prompt(contenido)
    return _generate_from_prompt(prompt, modelo, temperature=0.35, max_tokens=420)


def generate_feedback(preguntas_y_respuestas: str, modelo: str) -> str:
    """Compatibilidad retroactiva: mantiene la firma previa para feedback final."""
    return generate_test_feedback(preguntas_y_respuestas, modelo)