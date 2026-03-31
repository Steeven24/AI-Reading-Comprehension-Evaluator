import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Prefer explicit variable names and keep backward compatibility.
MODEL_GPT = os.getenv("MODEL_GPT") or os.getenv("GPT")
MODEL_LLAMA = os.getenv("MODEL_LLAMA") or os.getenv("LLAMA")