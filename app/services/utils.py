import fitz  # PyMuPDF
import spacy
from app.ollama_client import generate_content
from collections import Counter
import logging

logger = logging.getLogger('app')

# Load spaCy model and set max_length
nlp = spacy.load("en_core_web_sm")
nlp.max_length = 2000000

def extract_text_from_pdf(pdf_content):
    doc = fitz.open(stream=pdf_content, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_names(text):
    doc = nlp(text)
    names = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
    return names

def consolidate_names(names):
    # Frequency analysis
    name_counts = Counter(names)
    common_names = [name for name, count in name_counts.items() if count > 1]
    return common_names

def generate_character_details(name):
    prompt = f"Provide a detailed description for the character {name} including their name, sex, age, traits, behaviors, and a brief background summary in bullet points."
    details = generate_content(prompt)
    return details

def generate_book_details(text):
    prompt = f"Provide the book title, author, and genre of the following text: {text}"
    details = generate_content(prompt)
    return details

def get_summary(text):
    prompt = f"Summarize the following story: {text}"
    summary = generate_content(prompt)
    return summary
