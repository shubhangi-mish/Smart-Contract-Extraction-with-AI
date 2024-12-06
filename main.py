import os
import json
from pdf2txt import process_pdfs
from Extraction import extraction_prompt_from_dir  
from Zenskar_api import send_contract_to_zenskar

def main(pdf_directory, output_txt_directory, output_json_directory, summary_report_path):
    summary_report = {
        "total_files": 0,
        "successful_parses": 0,
        "errors": [],
        "file_errors": {}
    }
  
    try:
        process_pdfs(pdf_directory, output_txt_directory)
        summary_report["total_files"] = len([f for f in os.listdir(pdf_directory) if f.endswith('.pdf')])
    except Exception as e:
        summary_report["errors"].append(f"Error processing PDFs: {str(e)}")
        return  
    
    all_contracts = {}
    try:
        all_contracts = extraction_prompt_from_dir(output_txt_directory)
        summary_report["successful_parses"] += len(all_contracts)
    except Exception as e:
        summary_report["errors"].append(f"Error extracting data from text files: {str(e)}")
    
    for filename, extracted_data in all_contracts.items():
        base_filename = os.path.basename(filename).split('.')[0]
        output_json_path = os.path.join(output_json_directory, f"{base_filename}.json")
        try:
            with open(output_json_path, 'w', encoding='utf-8') as json_file:
                json.dump(extracted_data, json_file, indent=4)
        except Exception as e:
            error_message = f"Error saving data for {filename}: {str(e)}"
            summary_report["errors"].append(error_message)
            summary_report["file_errors"][filename] = error_message
    
    '''
    for contract in all_contracts.values():
        response = send_contract_to_zenskar(contract)
        print(f"API Response: {response}")
    '''
    
    try:
        with open(summary_report_path, 'w', encoding='utf-8') as summary_file:
            json.dump(summary_report, summary_file, indent=4)
        print(f"Saved summary report to {summary_report_path}")
    except Exception as e:
        print(f"Error saving summary report: {str(e)}")

if __name__ == "__main__":
    pdf_directory = r"C:\Users\Shubhangi Mishra\Desktop\Zenskar_Shubhangi_Mishra\Smart Contracts"
    output_txt_directory = r"C:\Users\Shubhangi Mishra\Desktop\Zenskar_Shubhangi_Mishra\SM_Extracted"
    output_json_directory = r"C:\Users\Shubhangi Mishra\Desktop\Zenskar_Shubhangi_Mishra\SM_JSON"
    summary_report_path = r"C:\Users\Shubhangi Mishra\Desktop\Zenskar_Shubhangi_Mishra\summary_report.json"

    os.makedirs(output_txt_directory, exist_ok=True)
    os.makedirs(output_json_directory, exist_ok=True)
    
    main(pdf_directory, output_txt_directory, output_json_directory, summary_report_path)
