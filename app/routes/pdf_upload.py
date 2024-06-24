from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.character import process_character_details, save_character_to_db
from app.services.utils import extract_text_from_pdf, extract_names, consolidate_names, generate_book_details, get_summary
import logging
import logging.config
import os

router = APIRouter()
logging_config_path = os.path.join(os.path.dirname(__file__), '..', 'logging.conf')
logging.config.fileConfig(logging_config_path)
logger = logging.getLogger('app')

@router.post("/upload_pdf/")
async def upload_pdf(file: UploadFile = File(...), db: Session = Depends(get_db)):
    logger.info("Upload started.")
    try:
        if not file.filename.endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Invalid file type. Only PDFs are allowed.")
        
        # Read the PDF file
        pdf_content = await file.read()
        text = extract_text_from_pdf(pdf_content)
        
        logger.info("Upload finished. Gathering chunks to send to Agent.")
        
        # Extract names and consolidate them
        names = extract_names(text)
        significant_names = consolidate_names(names)
        logger.info(f"Significant Names: {significant_names}")
        
        # Get book details
        book_details = generate_book_details(text)
        book_details_dict = parse_book_details(book_details)
        logger.info(f"Book Details: {book_details_dict}")
        
        # Process and save character details
        detailed_summaries = process_character_details(significant_names, db, book_details_dict)
        
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


def parse_book_details(details):
    details_dict = {}
    for line in details.split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            details_dict[key.strip().replace('**', '').lower()] = value.strip()
    return details_dict
