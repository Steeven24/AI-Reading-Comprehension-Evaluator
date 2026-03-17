from groq import Groq
from config.settings import GROQ_API_KEY
from .prompt_engine import build_questions_prompt

def generate_questions(texto, modelo):
    if not GROQ_API_KEY:
        raise ValueError("Falta GROQ_API_KEY. Configúrala como variable de entorno.")

    client = Groq(api_key=GROQ_API_KEY)

    prompt = build_questions_prompt(texto)

    completion = client.chat.completions.create(
        model=modelo,
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_completion_tokens=500
    )

    return completion.choices[0].message.content