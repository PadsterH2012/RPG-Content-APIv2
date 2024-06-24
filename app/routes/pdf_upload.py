from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.ollama_client import generate_content
import fitz  # PyMuPDF
import logging
import spacy
import random
from collections import Counter

logger = logging.getLogger(__name__)

router = APIRouter()

# Load spaCy model and set max_length
nlp = spacy.load("en_core_web_sm")
nlp.max_length = 2000000

def extract_names(text):
    doc = nlp(text)
    names = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
    return names

def get_summary(text):
    prompt = f"Summarize the following story: {text}"
    summary = generate_content(prompt)
    return summary

def consolidate_names(names):
    # Frequency analysis
    name_counts = Counter(names)
    common_names = [name for name, count in name_counts.items() if count > 1]

    # Contextual matching: Here we would add more sophisticated context matching logic if needed
    # For simplicity, assume names appearing frequently are significant
    return common_names

def split_text(text, chunk_size=100000):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

def generate_character_details(name):
    prompt = f"Provide a detailed description for the character {name} including their name, sex, age, traits, behaviors, and a brief background summary in bullet points."
    details = generate_content(prompt)
    return details

@router.post("/upload_pdf/")
async def upload_pdf(file: UploadFile = File(...), db: Session = Depends(get_db)):
    logger.info("Upload started.")
    try:
        if not file.filename.endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Invalid file type. Only PDFs are allowed.")
        
        # Read the PDF file
        pdf_content = await file.read()
        doc = fitz.open(stream=pdf_content, filetype="pdf")
        
        # Extract text from the PDF
        text = ""
        for page in doc:
            text += page.get_text()
        
        logger.info("Upload finished. Gathering chunks to send to Agent.")
        
        # Split text into chunks if it exceeds spaCy's max_length
        if len(text) > nlp.max_length:
            chunks = split_text(text, chunk_size=nlp.max_length)
            names = []
            for chunk in chunks:
                names.extend(extract_names(chunk))
        else:
            names = extract_names(text)
        
        # Consolidate names
        significant_names = consolidate_names(names)
        logger.info(f"Significant Names: {significant_names}")
        
        # Select five random names and generate details
        random_names = random.sample(significant_names, min(5, len(significant_names)))
        detailed_summaries = {}
        for i, name in enumerate(random_names, 1):
            logger.info(f"Agent checking character #{i}: {name}")
            summary = generate_character_details(name)
            if "I apologize" not in summary:  # If no information found, skip the character
                detailed_summaries[name] = summary
        
        # Get summary of the story
        summary = get_summary(text)
        logger.info(f"Story Summary: {summary}")
        
        return {
            "message": "PDF uploaded and processed successfully",
            "names": significant_names,
            "summary": summary,
            "detailed_summaries": detailed_summaries
        }
    except Exception as e:
        logger.error(f"Error processing PDF: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
