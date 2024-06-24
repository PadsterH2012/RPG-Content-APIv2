from sqlalchemy.orm import Session
from app.models.character import Character
from app.services.utils import generate_character_details
import logging
import random

logger = logging.getLogger('app')

def process_character_details(names, db: Session, book_details_dict):
    detailed_summaries = {}
    random_names = random.sample(names, min(5, len(names)))
    for i, name in enumerate(random_names, 1):
        logger.info(f"Agent checking character #{i}: {name}")
        summary = generate_character_details(name)
        if "I apologize" not in summary:
            details_dict = parse_character_details(summary)
            logger.info(f"Parsed Character Details: {details_dict}")
            if 'name' in details_dict and details_dict.get('name'):
                save_character_to_db(details_dict, db, book_details_dict)
                detailed_summaries[name] = details_dict
            else:
                logger.info(f"Character name is missing or invalid: {details_dict}")
    return detailed_summaries

def save_character_to_db(details_dict, db: Session, book_details_dict):
    if not db.query(Character).filter(Character.name == details_dict['name']).first():
        new_character = Character(
            name=details_dict.get('name'),
            sex=details_dict.get('sex', ''),
            age=details_dict.get('age', ''),
            traits=details_dict.get('traits', ''),
            behaviors=details_dict.get('behaviors', ''),
            background=details_dict.get('background', ''),
            book_title=book_details_dict.get('book title', ''),
            author=book_details_dict.get('author', ''),
            dialogue_examples=details_dict.get('dialogue examples', ''),
            genre=book_details_dict.get('genre', '')
        )
        db.add(new_character)
        db.commit()
        db.refresh(new_character)
        logger.info(f"Character {new_character.name} added to the database.")
    else:
        logger.info(f"Character already exists in the database: {details_dict.get('name')}")


def parse_character_details(details):
    details_dict = {}
    current_key = None
    current_value = []

    for line in details.split('\n'):
        line = line.strip().replace('**', '')  # Remove asterisks
        logger.debug(f"Parsing line: {line}")
        if not line:
            continue
        if ':' in line and line.split(':')[0].strip().lower() in ["name", "sex", "age", "traits", "behaviors", "background", "dialogue examples"]:
            if current_key and current_value:
                details_dict[current_key] = ' '.join(current_value).strip()
                logger.debug(f"Set {current_key} to {' '.join(current_value).strip()}")
            current_key = line.split(':')[0].strip().lower()
            current_value = [line.split(':', 1)[1].strip()]
        else:
            current_value.append(line.strip())

    if current_key and current_value:
        details_dict[current_key] = ' '.join(current_value).strip()
        logger.debug(f"Set {current_key} to {' '.join(current_value).strip()}")

    logger.debug(f"Final parsed details: {details_dict}")
    return details_dict

