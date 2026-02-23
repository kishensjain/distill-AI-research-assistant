import gradio as gr
import os
from openai import OpenAI, APIConnectionError
from dotenv import load_dotenv
from src.chunker import get_relevant_chunks

load_dotenv()

client = OpenAI(
    base_url="https://ollama.com/v1",
    api_key=os.getenv("OLLAMA_API_KEY")
)

MODEL = "gpt-oss:120b"


def build_system_prompt(relevant_content: str) -> str:
    return f"""You are a helpful research assistant.
Answer the user's question based on the following relevant excerpts from their research material.
If the answer isn't present, say so honestly.

--- CONTENT START ---
{relevant_content}
--- CONTENT END ---"""


def load_sources(sources_text: str, files):
    pass


def respond(user_message: str, history: list, chunks: list):
    if not chunks:
        history.append({"role": "user", "content": user_message})
        history.append(
            {"role": "assistant", "content": "⚠️ Please load some sources first."})
        yield history
        return

    relevant_content = get_relevant_chunks(user_message, chunks)

    messages = [
        {"role": "system", "content": build_system_prompt(relevant_content)},
        *history,
        {"role": "user", "content": user_message}
    ]

    history.append({"role": "user", "content": user_message})
    history.append({"role": "assistant", "content": ""})

    try:
        stream = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            stream=True
        )

        for chunk in stream:
            delta = chunk.choices[0].delta.content or ""
            history[-1]["content"] += delta
            yield history

    except APIConnectionError:
        history[-1]["content"] = "❌ Could not connect to Ollama. Run: ollama serve"
        yield history
    except Exception as e:
        history[-1]["content"] = f"❌ Unexpected error: {e}"
        yield history


def build_ui() -> gr.Blocks:
    with gr.Blocks(title="AI research assistant") as demo:
        gr.Markdown(
            "# 🔍 AI Research Assistant by Kishen\nLoad URLs or paste text, then ask questions about it.")

        chunks_state = gr.State([])

        with gr.Row():
            with gr.Column(scale=1):
                sources_input = gr.Textbox(
                    label="Sources",
                    placeholder="Enter one URL or text block per line...",
                    lines=5
                )
                file_input = gr.File(
                    label="Or upload PDF / Word files",
                    file_types=[".pdf", ".docx"],
                    file_count="multiple",
                )
                load_btn = gr.Button("Load Sources", variant="primary")
                load_output = gr.Textbox(
                    label="Load Status", lines=5, interactive=False)

            with gr.Column(scale=2):
                chatbot = gr.Chatbot(label="Chat", height=480)
                user_input = gr.Textbox(
                    label="Your question",
                    placeholder="Ask something about your sources...",
                )
                send_btn = gr.Button("Send", variant="primary")

            load_btn.click(
                fn=load_sources,
                inputs=[sources_input, file_input],
                outputs=[load_output, chunks_state]
            )

            send_btn.click(
                fn=respond,
                inputs=[user_input, chatbot, chunks_state],
                outputs=[chatbot]
            ).then(lambda: "", outputs=[user_input])

            user_input.submit(
                fn=respond,
                inputs=[user_input, chatbot, chunks_state],
                outputs=[chatbot]
            ).then(lambda: "", outputs=[user_input])

    return demo
