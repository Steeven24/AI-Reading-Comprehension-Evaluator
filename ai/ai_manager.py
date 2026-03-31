from groq import Groq
from config.settings import GROQ_API_KEY
from .prompt_engine import build_questions_prompt

def generate_questions(texto: str, modelo: str) -> str:
    if not GROQ_API_KEY:
        raise ValueError("Falta GROQ_API_KEY. Configúrala como variable de entorno.")
    if not modelo:
        raise ValueError("No se recibió un modelo válido para generar preguntas.")

    texto_limpio = (texto or "").strip()
    if not texto_limpio:
        raise ValueError("No hay texto para generar preguntas.")

    client = Groq(api_key=GROQ_API_KEY)

    prompt = build_questions_prompt(texto_limpio)

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