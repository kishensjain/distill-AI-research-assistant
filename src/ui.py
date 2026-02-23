import gradio as gr
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url = "https://ollama.com/v1",
    api_key = os.getenv("OLLAMA_API_KEY")
)

MODEL = "gpt-oss:120b"

def build_ui() -> gr.Blocks:
    with gr.Blocks() as demo:
        pass
    
    return demo