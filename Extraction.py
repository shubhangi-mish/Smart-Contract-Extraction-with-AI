import os
import json
import spacy
from openai import OpenAI
from Regex_nlp_validation import validate_contract_amount, extract_billing_frequency, extract_contract_id, extract_contract_type, extract_customer_name, extract_date, extract_payment_terms
from Evaluation_metrics import evaluate_extraction
from Zenskar_api import send_contract_to_zenskar

nlp = spacy.load("en_core_web_sm")

client = OpenAI(api_key='OPEN_AI_API_KEY') #removed while uploading to github 

def call_openai_api(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": "You are an assistant that extracts specific fields from text documents."},
                      {"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.7
        )
        message = response.choices[0].message.content
        
        return message if message.lower() != "null" else None
    except Exception as e:
        print(f"Error: {e}")
        return None

def read_file(file_path):
    try:
        with open(file_path, 'r', encoding="utf-8", errors="ignore") as file:
            return file.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return None
    
def extract_currency(order_form_text):
    prompt = f"Extract the currency of transaction from the following text and only give the currency abbreviation stictly (eg, USD,INR etc) if nothing give none.\n\n{order_form_text}"
    return call_openai_api(prompt)

def extract_contract_id(order_form_text):
    prompt = f"Extract the contract ID from the following text and only give the ID if nothing give none.\n\n{order_form_text}"
    return call_openai_api(prompt)

def extract_contract_id_reasoning(order_form_text):
    prompt = f"Include a reasoning log sentence for contract ID extraction result in one line only. do not make headings give only 1 line answers strictly\n\n{order_form_text}"
    return call_openai_api(prompt)

def extract_contract_id_confidence(order_form_text):
    prompt = f"Include the confidence level in number (0-1) for the extraction of the contract ID based on the provided text and give only the number strictly no headings no sentence.\n\n{order_form_text}"
    return call_openai_api(prompt)

def extract_customer_name(order_form_text):
    prompt = f"Extract the 'Client Company Name' from the following text and give only the name, nothing else.\n\n{order_form_text}"
    return call_openai_api(prompt)

def extract_customer_name_reasoning(order_form_text):
    prompt = f"Include a reasoning log sentence for customer name extraction and reason if not extracted in one line only do not make headings give only 1 line answers strictly.\n\n{order_form_text}"
    return call_openai_api(prompt)

def extract_customer_name_confidence(order_form_text):
    prompt = f"Include the confidence level in number (0-1) for the extraction of the customer name based on the provided text and give only the number strictly no headings no sentence.\n\n{order_form_text}"
    return call_openai_api(prompt)

def extract_contract_start_date(order_form_text):
    prompt = f"Extract the 'Date' which is the contract start date from the following text. Provide only the date in YYYY-MM-DD format strictly\n\n{order_form_text}"
    return call_openai_api(prompt)

def extract_contract_start_date_reasoning(order_form_text):
    prompt = f"Include a reasoning log sentence for contract start date extraction and reason if not extracted in one line only do not make headings give only 1 line answers strictly.\n\n{order_form_text}"
    return call_openai_api(prompt)

def extract_contract_start_date_confidence(order_form_text):
    prompt = f"Include the confidence level in number (0-1) for the extraction of the contract start date based on the provided text and give only the number strictly no headings no sentence.\n\n{order_form_text}"
    return call_openai_api(prompt)

def extract_contract_end_date(order_form_text):
    prompt = f"Extract the 'End of service date' from the following text. If it is not directly mentioned, determine it based on the provided renewal terms and give only the date in YYYY-MM-DD format strictly:\n\n{order_form_text}"
    return call_openai_api(prompt)

def extract_contract_end_date_reasoning(order_form_text):
    prompt = f"Include a reasoning log sentence for contract end date extraction and reason if not extracted in one line only do not make headings give only 1 line answers strictly.\n\n{order_form_text}"
    return call_openai_api(prompt)

def extract_contract_end_date_confidence(order_form_text):
    prompt = f"Include the confidence level in number (0-1) for the extraction of the contract end date based on the provided text and give only the number strictly no headings no sentence.\n\n{order_form_text}"
    return call_openai_api(prompt)

def extract_payment_terms(order_form_text):
    prompt = f"Extract the 'Payment Terms' from the following text. Provide only the term \n\n{order_form_text}"
    return call_openai_api(prompt)

def extract_payment_terms_reasoning(order_form_text):
    prompt = f"Include a reasoning log sentence for payment terms extraction and reason if not extracted in one line only do not make headings give only 1 line answers strictly.\n\n{order_form_text}"
    return call_openai_api(prompt)

def extract_payment_terms_confidence(order_form_text):
    prompt = f"Include the confidence level in number (0-1) for the extraction of the payment terms based on the provided text and give only the number strictly no headings no sentence.\n\n{order_form_text}"
    return call_openai_api(prompt)

def extract_contract_amount(order_form_text):
    prompt = f"Extract the total 'Contract Amount' for professional services from the following text. Provide only the amount directly \n\n{order_form_text}"
    return call_openai_api(prompt)

def extract_contract_amount_reasoning(order_form_text):
    prompt = f"Include a reasoning log sentence for contract amount extraction and reason if not extracted in one line only do not make headings give only 1 line answers strictly.\n\n{order_form_text}"
    return call_openai_api(prompt)

def extract_contract_amount_confidence(order_form_text):
    prompt = f"Include the confidence level in number (0-1) for the extraction of the contract amount based on the provided text and give only the number strictly no headings no sentence.\n\n{order_form_text}"
    return call_openai_api(prompt)

def extract_billing_frequency(order_form_text):
    prompt = f"Extract the 'Billing Frequency' from the following text. Only one word is needed \n\n{order_form_text}"
    return call_openai_api(prompt)

def extract_billing_frequency_reasoning(order_form_text):
    prompt = f"Include a reasoning log sentence for billing frequency extraction and reason if not extracted in one line only do not make headings give only 1 line answers strictly.\n\n{order_form_text}"
    return call_openai_api(prompt)

def extract_billing_frequency_confidence(order_form_text):
    prompt = f"Include the confidence level in number (0-1) for the extraction of the billing frequency based on the provided text and give only the number strictly no headings no sentence.\n\n{order_form_text}"
    return call_openai_api(prompt)

def extract_contract_type(order_form_text):
    prompt = f"Extract the 'Contract Type' from the following text. The contract type includes the categories such as 'Professional Services' and 'Subscription Services'. Provide only the type along \n\n{order_form_text}"
    return call_openai_api(prompt)

def extract_contract_type_reasoning(order_form_text):
    prompt = f"Include a reasoning log sentence for contract type extraction and reason if not extracted in one line only do not make headings give only 1 line answers strictly.\n\n{order_form_text}"
    return call_openai_api(prompt)

def extract_contract_type_confidence(order_form_text):
    prompt = f"Include the confidence level in number (0-1) for the extraction of the contract type based on the provided text and give only the number strictly no headings no sentence.\n\n{order_form_text}"
    return call_openai_api(prompt)

    
def extract_all_data(order_form_text):
    extracted_data = {
        "Currency": extract_currency(order_form_text),

        "Contract ID": extract_contract_id(order_form_text),
        "Contract ID Reasoning": extract_contract_id_reasoning(order_form_text),
        "Contract ID Confidence": extract_contract_id_confidence(order_form_text),
        
        "Customer Name": extract_customer_name(order_form_text),
        "Customer Name Reasoning": extract_customer_name_reasoning(order_form_text),
        "Customer Name Confidence": extract_customer_name_confidence(order_form_text),
        
        "Contract Start Date": extract_contract_start_date(order_form_text),
        "Contract Start Date Reasoning": extract_contract_start_date_reasoning(order_form_text),
        "Contract Start Date Confidence": extract_contract_start_date_confidence(order_form_text),
        
        "Contract End Date": extract_contract_end_date(order_form_text),
        "Contract End Date Reasoning": extract_contract_end_date_reasoning(order_form_text),
        "Contract End Date Confidence": extract_contract_end_date_confidence(order_form_text),
        
        "Payment Terms": extract_payment_terms(order_form_text),
        "Payment Terms Reasoning": extract_payment_terms_reasoning(order_form_text),
        "Payment Terms Confidence": extract_payment_terms_confidence(order_form_text),
        
        "Contract Amount": extract_contract_amount(order_form_text),
        "Contract Amount Reasoning": extract_contract_amount_reasoning(order_form_text),
        "Contract Amount Confidence": extract_contract_amount_confidence(order_form_text),
        
        "Billing Frequency": extract_billing_frequency(order_form_text),
        "Billing Frequency Reasoning": extract_billing_frequency_reasoning(order_form_text),
        "Billing Frequency Confidence": extract_billing_frequency_confidence(order_form_text),
        
        "Contract Type": extract_contract_type(order_form_text),
        "Contract Type Reasoning": extract_contract_type_reasoning(order_form_text),
        "Contract Type Confidence": extract_contract_type_confidence(order_form_text),
    }


    contract_data = {
        "Currency":extracted_data.get("Currency", ""),

        "Contract ID": {
            "extracted_value": extracted_data.get("Contract ID", ""),
            "reasoning": extracted_data.get("Contract ID Reasoning", ""),
            "confidence": extracted_data.get("Contract ID Confidence", "")
        },
        "Customer Name": {
            "extracted_value": extracted_data.get("Customer Name", ""),
            "reasoning": extracted_data.get("Customer Name Reasoning", ""),
            "confidence": extracted_data.get("Customer Name Confidence", "")
        },
        "Contract Start Date": {
            "extracted_value": extracted_data.get("Contract Start Date", ""),
            "reasoning": extracted_data.get("Contract Start Date Reasoning", ""),
            "confidence": extracted_data.get("Contract Start Date Confidence", "")
        },
        "Contract End Date": {
            "extracted_value": extracted_data.get("Contract End Date", ""),
            "reasoning": extracted_data.get("Contract End Date Reasoning", ""),
            "confidence": extracted_data.get("Contract End Date Confidence", "")
        },
        "Payment Terms": {
            "extracted_value": extracted_data.get("Payment Terms", ""),
            "reasoning": extracted_data.get("Payment Terms Reasoning", ""),
            "confidence": extracted_data.get("Payment Terms Confidence", "")
        },
        "Contract Amount": {
            "extracted_value": extracted_data.get("Contract Amount", ""),
            "reasoning": extracted_data.get("Contract Amount Reasoning", ""),
            "confidence": extracted_data.get("Contract Amount Confidence", "")
        },
        "Metadata": {
            "Billing Frequency": {
                "extracted_value": extracted_data.get("Billing Frequency", ""),
                "reasoning": extracted_data.get("Billing Frequency Reasoning", ""),
                "confidence": extracted_data.get("Billing Frequency Confidence", "")
            },
            "Contract Type": {
                "extracted_value": extracted_data.get("Contract Type", ""),
                "reasoning": extracted_data.get("Contract Type Reasoning", ""),
                "confidence": extracted_data.get("Contract Type Confidence", "")
            }
        }
    }
    evaluate_extraction(contract_data)
    send_contract_to_zenskar(contract_data)
    return contract_data


def validate_extracted_data(extracted_data, order_form_text):
    if not extracted_data.get("Currency"):
        extracted_data["Currency"]= extract_currency(order_form_text)
    if not extracted_data.get("Contract ID"):
        extracted_data["Contract ID"] = extract_contract_id(order_form_text)
    if not extracted_data.get("Customer Name"):
        extracted_data["Customer Name"] = extract_customer_name(order_form_text)
    if not extracted_data.get("Contract Start Date"):
        extracted_data["Contract Start Date"] = extract_contract_start_date(order_form_text)
    if not extracted_data.get("Contract End Date"):
        extracted_data["Contract End Date"] = extract_contract_end_date(order_form_text)
    if not extracted_data.get("Payment Terms"):
        extracted_data["Payment Terms"] = extract_payment_terms(order_form_text)
    if not extracted_data.get("Contract Amount"):
        extracted_data["Contract Amount"] = extract_contract_amount(order_form_text)
    if not extracted_data.get("Billing Frequency"):
        extracted_data["Billing Frequency"] = extract_billing_frequency(order_form_text)
    if not extracted_data.get("Contract Type"):
        extracted_data["Contract Type"] = extract_contract_type(order_form_text)
    
    return extracted_data
    


def extraction_prompt_from_dir(text_directory):
    all_contracts = {}
    if not os.path.isdir(text_directory):
        print(f"Error: {text_directory} is not a valid directory.")
        return all_contracts

    try:
        for text_file in os.listdir(text_directory):
            file_path = os.path.join(text_directory, text_file)
            if os.path.isfile(file_path) and text_file.endswith(".txt"):
                order_form_text = read_file(file_path)
                if order_form_text:
                    extracted_data = extract_all_data(order_form_text)
                    all_contracts[text_file] = extracted_data
        return all_contracts
    except Exception as e:
        print(f"Error: {e}")
        return all_contracts

def save_contract_json(extracted_data, json_directory):
    try:
        os.makedirs(json_directory, exist_ok=True)

        for filename, contract_data in extracted_data.items():
            json_path = os.path.join(json_directory, f"{filename}.json")
            with open(json_path, 'w', encoding='utf-8') as json_file:
                json.dump(contract_data, json_file, ensure_ascii=False, indent=4)
            print(f"Contract data for {filename} saved successfully.")
    except Exception as e:
        print(f"Error saving contract data: {e}")

