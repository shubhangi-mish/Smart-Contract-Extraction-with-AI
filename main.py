import os
import json
from pdf2txt import process_pdfs
from Extraction import extraction_prompt_from_dir
from Zenskar_api import send_contract_to_zenskar

def main(pdf_directory, output_txt_directory, output_json_directory, summary_json_path):
    # Create output directories if they don't exist
    os.makedirs(output_txt_directory, exist_ok=True)
    os.makedirs(output_json_directory, exist_ok=True)

    # Process PDFs and handle batch processing
    all_contracts = {}
    success_count = 0
    error_count = 0
    error_log = []

    # Step 1: Process all PDF files in the directory
    try:
        process_pdfs(pdf_directory, output_txt_directory)
        print(f"Successfully processed PDFs in {pdf_directory}")
    except Exception as e:
        print(f"Error processing PDFs: {str(e)}")

    # Step 2: Extract data from each text file in the output directory
    for filename in os.listdir(output_txt_directory):
        if filename.endswith('.txt'):
            file_path = os.path.join(output_txt_directory, filename)
            try:
                extracted_data = extraction_prompt_from_dir(file_path)  # assuming this function processes a single file
                all_contracts[filename] = extracted_data
                success_count += 1
                print(f"Successfully extracted data from {filename}")
            except Exception as e:
                error_count += 1
                error_log.append(f"Error extracting data from {filename}: {str(e)}")
                print(f"Error extracting data from {filename}: {str(e)}")

    # Step 3: Save extracted data to JSON files
    for filename, extracted_data in all_contracts.items():
        base_filename = os.path.basename(filename).split('.')[0]
        output_json_path = os.path.join(output_json_directory, f"{base_filename}.json")
        try:
            with open(output_json_path, 'w', encoding='utf-8') as json_file:
                json.dump(extracted_data, json_file, indent=4)
            print(f"Saved extracted data to {output_json_path}")
        except Exception as e:
            error_count += 1
            error_log.append(f"Error saving {filename} to JSON: {str(e)}")
            print(f"Error saving {filename} to JSON: {str(e)}")

    # Generate Summary Report in JSON format
    summary_report = {
        "total_pdfs_processed": success_count + error_count,
        "successfully_parsed_contracts": success_count,
        "errors_occurred": error_count,
        "error_log": error_log
    }

    # Save the summary report as a JSON file
    with open(summary_json_path, 'w', encoding='utf-8') as summary_file:
        json.dump(summary_report, summary_file, indent=4)
    
    print(f"\nSummary report saved to {summary_json_path}")

if __name__ == "__main__":
    pdf_directory = r"C:\Users\Shubhangi Mishra\Desktop\Zenskar_Shubhangi_Mishra\Smart Contracts"
    output_txt_directory = r"C:\Users\Shubhangi Mishra\Desktop\Zenskar_Shubhangi_Mishra\SM_Extracted"
    output_json_directory = r"C:\Users\Shubhangi Mishra\Desktop\Zenskar_Shubhangi_Mishra\SM_JSON"
    summary_json_path = r"C:\Users\Shubhangi Mishra\Desktop\Zenskar_Shubhangi_Mishra\SM_summary_report.json"

    main(pdf_directory, output_txt_directory, output_json_directory, summary_json_path)
