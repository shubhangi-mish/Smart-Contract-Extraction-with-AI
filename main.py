import os
from pdf2txt import process_pdfs
from Extraction import extraction_prompt, extraction_prompt_from_dir  
from Zenskar_api import send_contract_to_zenskar
import json

def main(pdf_directory, output_txt_directory, output_json_directory):
  
    process_pdfs(pdf_directory, output_txt_directory)
    
    all_contracts = extraction_prompt_from_dir(output_txt_directory)

    for filename, extracted_data in all_contracts.items():
        base_filename = os.path.basename(filename).split('.')[0]
        output_json_path = os.path.join(output_json_directory, f"{base_filename}.json")
        with open(output_json_path, 'w', encoding='utf-8') as json_file:
            json.dump(extracted_data, json_file, indent=4)
        print(f"Saved extracted data to {output_json_path}")
    
    '''
    # Step 4: Send extracted data to the API
    for contract in all_contracts.values():
        response = send_contract_to_zenskar(contract)
        print(f"API Response: {response}")
    '''

if __name__ == "__main__":
    pdf_directory = r"C:\Users\Shubhangi Mishra\Desktop\Zenskar_Shubhangi_Mishra\Smart Contracts"
    output_txt_directory = r"C:\Users\Shubhangi Mishra\Desktop\Zenskar_Shubhangi_Mishra\SM_Extracted"
    output_json_directory = r"C:\Users\Shubhangi Mishra\Desktop\Zenskar_Shubhangi_Mishra\SM_JSON"

    os.makedirs(output_txt_directory, exist_ok=True)
    os.makedirs(output_json_directory, exist_ok=True)
    
    main(pdf_directory, output_txt_directory, output_json_directory)
