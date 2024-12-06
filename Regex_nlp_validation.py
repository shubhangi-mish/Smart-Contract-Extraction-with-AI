import re
import spacy

nlp = spacy.load("en_core_web_sm")

def validate_contract_amount(amount_str):
    pattern = r'(\$|USD|EUR)?\s?(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)'
    match = re.search(pattern, amount_str)
    if match:
        return match.group(0)
    return None

def extract_date(text):
    pattern = r'\b(\d{1,2}[-/thstndrd]{0,2}\s?[A-Za-z]{3,9}\s?\d{4}|\d{4}[-/]\d{2}[-/]\d{2})\b'
    match = re.search(pattern, text)
    return match.group(0) if match else None

def extract_contract_id(text):
    pattern = r'\b[Cc]ontract\s?[ID|No.]*[:\s]*([A-Za-z0-9-]+)\b'
    match = re.search(pattern, text)
    return match.group(1) if match else None

def extract_customer_name(text):
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "ORG": 
            return ent.text
    return None

def extract_payment_terms(text):
    pattern = r'\b(?:Net\s*\d{1,3}|Due\swithin\s\d{1,3}\sdays)\b'
    match = re.search(pattern, text)
    return match.group(0) if match else None

def extract_billing_frequency(text):
    pattern = r'\b(monthly|quarterly|annually|yearly|bi-weekly|weekly|daily)\b'
    match = re.search(pattern, text, re.IGNORECASE)
    return match.group(0).lower() if match else None

def extract_contract_type(text):
    pattern = r'\b(Professional Services|Subscription Services)\b'
    match = re.search(pattern, text, re.IGNORECASE)
    return match.group(0) if match else None