import os
import pdfplumber
import fitz  # PyMuPDF
from ocr import ocr_pdf_to_text

def pdf_to_text(file_path):
    text = ""
    try:
        document = fitz.open(file_path)
        for page_num in range(len(document)):
            page = document.load_page(page_num)
            page_text = page.get_text()
            if page_text:
                text += page_text
    except Exception as e:
        print(f"Error reading PDF file '{file_path}' with PyMuPDF: {e}")
    return text

# Fallback function to read PDF files using pdfplumber, in case fitz fails.
def fallback_pdf_to_text(file_path):
    text = ""
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
    except Exception as e:
        print(f"Error reading PDF file '{file_path}' with pdfplumber: {e}")
    return text

def save_text_to_file(text, output_path):
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(text)

def convert_pdf_to_text(file_path, output_txt_dir):
    ext = os.path.splitext(file_path)[1].lower()
    text = ""
    
    if ext == '.pdf':
        text = pdf_to_text(file_path)
        if not text.strip():  # If PyMuPDF fails, use pdfplumber
            text = fallback_pdf_to_text(file_path)
        if not text.strip():  # If both fail, use OCR
            text = ocr_pdf_to_text(file_path)
    else:
        print(f"Unsupported file format: {file_path}")
        return
    
    if not text.strip():
        print(f"No text extracted from {file_path}")
        return
    

    base_filename = os.path.basename(file_path).split('.')[0]
    output_txt_path = os.path.join(output_txt_dir, f"{base_filename}.txt")
    save_text_to_file(text, output_txt_path)
    print(f"Saved {file_path} as {output_txt_path}")
    return output_txt_path

def process_pdfs(pdf_dir, output_txt_dir):
    os.makedirs(output_txt_dir, exist_ok=True)
    processed_files = []

    for filename in os.listdir(pdf_dir):
        if filename.endswith(".pdf"):
            file_path = os.path.join(pdf_dir, filename)
            print(f"Processing file: {file_path}")
            output_txt_path = convert_pdf_to_text(file_path, output_txt_dir)
            if output_txt_path:
                processed_files.append(output_txt_path)

    print("All PDF files have been converted to .txt files.")
    return processed_files
