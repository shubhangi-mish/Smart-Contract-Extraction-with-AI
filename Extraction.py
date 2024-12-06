import os
import json
import spacy
from openai import OpenAI
from Regex_nlp_validation import validate_contract_amount, extract_billing_frequency, extract_contract_id, extract_contract_type, extract_customer_name, extract_date, extract_payment_terms

nlp = spacy.load("en_core_web_sm")

client = OpenAI(api_key='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')

def call_openai_api(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": "You are an assistant that extracts specific fields from text documents."},
                      {"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.7
        )
        message = response.choices[0].message.content.strip()
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

def extraction_prompt(order_form_text):
  
    prompts = {
        "Contract ID": f"Extract the 'Order Form Number' from the following text and only give the ID if nothing then Null:\n\n{order_form_text}",
        "Customer Name": f"Extract the 'Client Company Name' from the following text and give only the name nothing else:\n\n{order_form_text}",
        "Contract Start Date": f"Extract the 'Date' which is the contract start date from the following text: give only the date and in format YYYY-MM-DD\n\n{order_form_text}",
        "Contract End Date": f"Extract the 'End of service date' from the following text. If it is not directly mentioned, determine it based on the provided renewal terms and give only the date no words in the format YYYY-MM-DD:\n\n{order_form_text}",
        "Payment Terms": f"Extract the 'Payment Terms' from the following text: give only the term no sentences\n\n{order_form_text}",
        "Contract Amount": f"Extract the total 'Contract Amount' for professional services from the following text. This should be found under the 'Total' for 'Professional Services', give only the amount directly:\n\n{order_form_text}",
        "Billing Frequency": f"Extract the 'Billing Frequency' from the following text: only one word\n\n{order_form_text}",
        "Contract Type": f"Extract the 'Contract Type' from the following text. The contract type includes the categories such as 'Professional Services' and 'Subscription Services' there can be only one give that only no sentences:\n\n{order_form_text}"
    }

    extracted_data = {field: call_openai_api(prompt) for field, prompt in prompts.items()}

    if not extracted_data["Contract ID"]:
        extracted_data["Contract ID"] = extract_contract_id(order_form_text)
    if not extracted_data["Customer Name"]:
        extracted_data["Customer Name"] = extract_customer_name(order_form_text)
    if not extracted_data["Contract Start Date"]:
        extracted_data["Contract Start Date"] = extract_date(order_form_text)
    if not extracted_data["Contract End Date"]:
        extracted_data["Contract End Date"] = extract_date(order_form_text)
    if not extracted_data["Payment Terms"]:
        extracted_data["Payment Terms"] = extract_payment_terms(order_form_text)
    if not extracted_data["Contract Amount"]:
        extracted_data["Contract Amount"] = validate_contract_amount(extracted_data.get("Contract Amount", ""))
    if not extracted_data["Billing Frequency"]:
        extracted_data["Billing Frequency"] = extract_billing_frequency(order_form_text)
    if not extracted_data["Contract Type"]:
        extracted_data["Contract Type"] = extract_contract_type(order_form_text)

    contract_data = {
        "Contract ID": extracted_data.get("Contract ID"),
        "Customer Name": extracted_data.get("Customer Name"),
        "Contract Start Date": extracted_data.get("Contract Start Date"),
        "Contract End Date": extracted_data.get("Contract End Date"),
        "Payment Terms": extracted_data.get("Payment Terms"),
        "Contract Amount": extracted_data.get("Contract Amount"),
        "Metadata": {
            "Billing Frequency": extracted_data.get("Billing Frequency"),
            "Contract Type": extracted_data.get("Contract Type")
        }
    }

    return contract_data

def extraction_prompt_from_dir(text_directory):
    all_contracts = {}
    for text_file in os.listdir(text_directory):
        if text_file.endswith(".txt"):
            file_path = os.path.join(text_directory, text_file)
            order_form_text = read_file(file_path)
            if order_form_text:
                extracted_data = extraction_prompt(order_form_text)
                all_contracts[text_file] = extracted_data
    return all_contracts
