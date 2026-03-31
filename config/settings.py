import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Prefer explicit variable names and keep backward compatibility.
MODEL_GPT = os.getenv("MODEL_GPT") or os.getenv("GPT")
MODEL_LLAMA = os.getenv("MODEL_LLAMA") or os.getenv("LLAMA")
MODEL_GEMINI = (
	os.getenv("MODEL_GEMINI")
	or os.getenv("GEMINI_MODEL_NAME")
	or os.getenv("GEMINI")
	or "gemini-2.5-flash"
)