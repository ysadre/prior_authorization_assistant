from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from pdf_parser import extract_text_from_pdf
import PyPDF2

model = SentenceTransformer("all-MiniLM-L6-v2")
pdf_text = extract_text_from_pdf("evicore_guidelines.pdf")
guideline_sentences = pdf_text.split("\n")

embeddings = model.encode(guideline_sentences)
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings))

def run_vector_search(diagnosis, procedure):
    """Find relevant sections from the guidelines PDF based on diagnosis & procedure."""
    pdf_path = "pdfs/evicore_guidelines.pdf"
    extracted_text = []
    page_numbers = []

    with open(pdf_path, "rb") as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text and (diagnosis.lower() in text.lower() or procedure.lower() in text.lower()):
                extracted_text.append(text)
                page_numbers.append(i + 1)  # Page numbers start from 1

    return extracted_text, page_numbers

def search_guideline(diagnosis, procedure):
    """Fetch the most relevant text and page numbers from the PDF."""
    relevant_text, pages = run_vector_search(diagnosis, procedure)

    if not relevant_text:
        return [], []

    return relevant_text, pages 