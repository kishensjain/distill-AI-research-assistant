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