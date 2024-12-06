# Contract Parsing and Integration with Zenskar API

## Project Overview

This project automates the extraction, validation, and transformation of key fields from contract documents using large language models (LLMs). The goal is to parse unstructured contract data and extract important details like contract IDs, dates, customer names, payment terms, and other metadata.

### What It Does:

1. **Contract Parsing using LLMs and Dynamic Prompts:**  
   The project uses large language models (e.g., GPT-4) to extract key contract details. Custom prompts guide the model in identifying fields like contract ID, customer name, contract dates, payment terms, contract amount, and metadata.

2. **Hybrid Approach for Data Validation:**  
   Combines the flexibility of LLMs for understanding context and extracting unstructured data, with deterministic methods like regex and NLP techniques for validation.

3. **Data Transformation and Integration:**  
   Validated contract data is integrated with the Zenskar Contract API for further processing and storage.  
   **Note:** Zenskar requires an organization account to generate an API key, so this part of the code is non-functional without one.

## Project File Structure and Description

### Directories

1. **`Contracts_Highlighted/`**  
   Stores PDF contracts with overlays highlighting the extracted text.

2. **`Contracts/`**  
   Contains all raw contract PDFs for processing.

3. **`Contracts_JSON/`**  
   Holds JSON files of the extracted and validated contract data.

4. **`Contracts_Txt/`**  
   Contains text files extracted from the PDFs, created by the `pdf2txt.py` script.

### Files

1. **`main.py`**  
   Main entry point for executing the code. Run with `python run main.py`.

2. **`pdf2txt.py`**  
   Converts PDF files to text. Calls `ocr.py` as a fallback for scanned PDFs.

3. **`ocr.py`**  
   Fallback script for extracting text using OCR when PDF conversion fails.

4. **`Extraction.py`**  
   Extracts structured data from text using LLMs with dynamic prompts.

5. **`regex_nlp_validation.py`**  
   Validates extracted data using regex and NLP techniques.

6. **`json_to_pdf.py`**  
   Overlays extracted text onto PDFs, saving highlighted versions.

7. **`send_to_zenskar.py`**  
   Sends validated JSON data to the Zenskar Contract API.

8. **`evaluation_metrics.py`**  
   Evaluates the extraction performance with precision, recall, accuracy, and F1 score.

## Tools Used

- **GPT-4** (gpt-4o-mini)
- **SpaCy** for NLP tasks
- **Matplotlib** and **Scikit-Learn** for plotting evaluation metrics
- **Dynamic Prompts** for flexible LLM queries

## Installation Instructions

To set up the project, follow these steps:

### 1. Clone the Repository

First, clone the repository to your local machine:

```bash
git clone <repository_url>
cd <project_directory>'''

## Installation Guide

To set up the project and run it locally, follow the steps below:

### 2. Create a Virtual Environment

It's highly recommended to use a virtual environment to isolate your dependencies. You can create and activate one using the following commands:

#### On Windows:
```bash
python -m venv venv
.\venv\Scripts\activate

