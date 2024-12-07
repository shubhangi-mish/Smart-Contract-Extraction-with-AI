import re
import spacy
from datetime import datetime

nlp = spacy.load("en_core_web_sm")

def validate_currency(text):
    currency_patterns = r'(\$|USD|EUR|GBP|JPY|AUD|CAD|CHF|INR|CNY|NZD|SEK|NOK|DKK|ZAR|BRL|MXN|SAR|HKD)?\s?(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)'
    match = re.search(currency_patterns, text)
    if match:
        return match.group(0)
    return None

def validate_contract_amount(amount_str):
    currency_patterns = r'(\$|USD|EUR|GBP|JPY|AUD|CAD|CHF|INR|CNY|NZD|SEK|NOK|DKK|ZAR|BRL|MXN|SAR|HKD)?\s?(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)'
    match = re.search(currency_patterns, amount_str)
    
    if match:
        currency = match.group(1) if match.group(1) else ""
        amount = match.group(2).replace(',', '')
        
        if '.' not in amount:
            amount += '.00'
        elif len(amount.split('.')[1]) != 2:
            amount = amount[:amount.index('.') + 3]
            
        return f"{currency} {amount}" if currency else amount
    
    return None

def validate_date(text):
    pattern = r'''
            \b(
            (?:\d{2}[-/]\d{2}[-/]\d{4}) |
            (?:\d{4}[-/]\d{2}[-/]\d{2}) |
            (?:\d{1,2}(?:st|nd|rd|th)?\s?[A-Za-z]{3,9}\s?,?\s?\d{4}) |
            (?:[A-Za-z]{3,9}\s?\d{1,2}(?:st|nd|rd|th)?\s?,?\s?\d{4}) |
            (?:[A-Za-z]{3,9}\s?\d{4})
            )\b
        '''
    match = re.search(pattern, text, re.VERBOSE)
    
    if match:
        date_str = match.group(0)
        
        for fmt in ['%d-%m-%Y', '%d/%m/%Y', '%Y-%m-%d', '%Y/%m/%d', '%d %B %Y', '%B %d, %Y', '%B %Y']:
            try:
                parsed_date = datetime.strptime(date_str, fmt)
                return parsed_date.strftime('%Y-%m-%d')
            except ValueError:
                continue
        
    return None

def validate_contract_id(text):
    pattern = r'\b[Cc]ontract\s?[ID|No.]*[:\s]*([A-Za-z0-9-]+)\b'
    match = re.search(pattern, text)
    return match.group(1) if match else None

def validate_customer_name(text):
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "ORG": 
            return ent.text
    return None

def validate_payment_terms(text):
    pattern = r'\b(?:Net\s*\d{1,3}|Due\swithin\s\d{1,3}\sdays)\b'
    match = re.search(pattern, text)
    return match.group(0) if match else None

def validate_billing_frequency(text):
    pattern = r'\b(monthly|quarterly|annually|yearly|bi-weekly|weekly|daily)\b'
    match = re.search(pattern, text, re.IGNORECASE)
    return match.group(0).lower() if match else None

def validate_contract_type(text):
    pattern = r'\b(Professional Services|Subscription Services)\b'
    match = re.search(pattern, text, re.IGNORECASE)
    return match.group(0) if match else None