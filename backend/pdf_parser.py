import fitz  

def extract_text_from_pdf(pdf_filename):
    pdf_path = f"pdfs/{pdf_filename}"
    with fitz.open(pdf_path) as doc:
        return "\n".join([page.get_text("text") for page in doc])

