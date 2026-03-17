from dotenv import load_dotenv
import os

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

MODEL_GPT = os.getenv("GPT")
MODEL_LLAMA = os.getenv("LLAMA")