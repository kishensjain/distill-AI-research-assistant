import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url = "https://ollama.com/v1",
    api_key = os.getenv("OLLAMA_API_KEY")
)

MODEL = "gpt-oss:120b"
