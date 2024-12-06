import easyocr
import numpy as np
from pdf2image import convert_from_path

reader = easyocr.Reader(['en'])

def ocr_pdf_to_text(file_path):
    extracted_text = ""
    try:
        pages = convert_from_path(file_path, 300)  
        for page in pages:
            
            page_np = np.array(page)
            
            
            result = reader.readtext(page_np)
            for detection in result:
                extracted_text += detection[1] + " "  
    except Exception as e:
        print(f"Error performing OCR on PDF file '{file_path}': {e}")
    return extracted_text
