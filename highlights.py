import os
import fitz  # PyMuPDF
import json

def highlight_extracted_values(pdf_path, json_path, highlighted_pdf_directory):
    with open(json_path, 'r') as file:
        extracted_data = json.load(file)

    doc = fitz.open(pdf_path)

    def process_extracted_data(data, page):
        if isinstance(data, dict):
            for field, field_data in data.items():
                if isinstance(field_data, dict):
                    process_extracted_data(field_data, page)
                else:
                    extracted_value = field_data.get("extracted_value", "") if isinstance(field_data, dict) else field_data
                    if extracted_value:
                        text_instances = page.search_for(extracted_value)
                        for inst in text_instances:
                            highlight = page.add_highlight_annot(inst)
                            highlight.set_colors(stroke=(1, 1, 0))
                            highlight.update()
                            
                            span = page.get_text("dict", clip=inst)   

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        process_extracted_data(extracted_data, page)

    output_pdf_path = os.path.join(highlighted_pdf_directory, pdf_path.split("\\")[-1].replace(".pdf", "_highlighted.pdf"))
    doc.save(output_pdf_path)
    print(f"Highlighted PDF saved as {output_pdf_path}")

def process_directory(pdf_directory, json_directory, highlighted_pdf_directory):
    pdf_files = [f for f in os.listdir(pdf_directory) if f.endswith('.pdf')]
    for pdf_file in pdf_files:
        base_filename = os.path.splitext(pdf_file)[0]
        pdf_path = os.path.join(pdf_directory, pdf_file)
        json_path = os.path.join(json_directory, f"{base_filename}.json")
        if os.path.exists(json_path):
            print(f"Processing {pdf_file} with its corresponding JSON file.")
            highlight_extracted_values(pdf_path, json_path, highlighted_pdf_directory)
        else:
            print(f"Warning: JSON file for {pdf_file} not found, skipping.")
