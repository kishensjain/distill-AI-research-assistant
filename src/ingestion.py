import requests
from bs4 import BeautifulSoup
from pypdf import PdfReader
from docx import Document

def load_text(source:str) -> str:
    """Accept either a URL or raw pasted text."""
    if source.startswith("http://") or source.startswith("https://"):
        print("Fetching URL...")
        return fetch_url(source) #function to be defined soon
    else:
        return source

def load_file(file_path:str) -> str:
    if file_path.endswith(".pdf"):
        return extract_pdf(file_path) #function to be defined soon
    elif file_path.endswith(".docx"):
        return extract_docx(file_path) #function to be defined soon
    else:
        return open(file_path, "r").read()