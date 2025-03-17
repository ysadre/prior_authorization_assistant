import fitz
import os

def extract_text_from_pdfs(pdf_folder):
    pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith(".pdf")] 
    extracted_texts = {}

    for pdf_file in pdf_files:
        pdf_path = os.path.join(pdf_folder, pdf_file)
        with fitz.open(pdf_path) as doc:
            extracted_texts[pdf_file] = "\n".join([page.get_text("text") for page in doc])
    return extracted_texts