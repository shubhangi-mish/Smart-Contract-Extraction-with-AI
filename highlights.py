import os
import fitz  # PyMuPDF
import json

def highlight_extracted_values(pdf_path, json_path, highlighted_pdf_directory):
    # Read the extracted data from the JSON file
    with open(json_path, 'r') as file:
        extracted_data = json.load(file)

    # Open the PDF
    doc = fitz.open(pdf_path)

    # Function to extract and highlight fields from JSON
    def process_extracted_data(data, page):
        if isinstance(data, dict):
            # Process each key-value pair in the dictionary
            for field, field_data in data.items():
                # Check if the field has nested data (e.g., 'Metadata')
                if isinstance(field_data, dict):
                    process_extracted_data(field_data, page)  # Recursively process nested fields
                else:
                    # Directly access extracted_value if it exists
                    extracted_value = field_data.get("extracted_value", "") if isinstance(field_data, dict) else field_data
                    
                    # Search for the extracted value in the PDF and highlight it
                    if extracted_value:  # Ensure that extracted_value is not empty
                        text_instances = page.search_for(extracted_value)
                        for inst in text_instances:
                            # Highlight the extracted value
                            highlight = page.add_highlight_annot(inst)
                            highlight.set_colors(stroke=(1, 1, 0))  # Yellow highlight
                            highlight.update()

    # Iterate over the pages and extracted data
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        process_extracted_data(extracted_data, page)

    # Save the modified PDF to the highlighted PDF directory
    output_pdf_path = os.path.join(highlighted_pdf_directory, pdf_path.split("\\")[-1].replace(".pdf", "_highlighted.pdf"))
    doc.save(output_pdf_path)

    print(f"Highlighted PDF saved as {output_pdf_path}")


def process_directory(pdf_directory, json_directory, highlighted_pdf_directory):
    # Get list of files in the directories
    pdf_files = [f for f in os.listdir(pdf_directory) if f.endswith('.pdf')]
    
    # Process each PDF file
    for pdf_file in pdf_files:
        base_filename = os.path.splitext(pdf_file)[0]  # Get the base filename without extension
        pdf_path = os.path.join(pdf_directory, pdf_file)
        json_path = os.path.join(json_directory, f"{base_filename}.json")  # JSON file with the same base name

        # Check if the corresponding JSON file exists
        if os.path.exists(json_path):
            print(f"Processing {pdf_file} with its corresponding JSON file.")
            highlight_extracted_values(pdf_path, json_path, highlighted_pdf_directory)
        else:
            print(f"Warning: JSON file for {pdf_file} not found, skipping.")


