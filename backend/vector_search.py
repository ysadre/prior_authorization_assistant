from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from pdf_parser import extract_text_from_pdfs
import PyPDF2
import os

# Load the sentence transformer model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Extract text from all PDFs in the "pdfs/" folder
pdf_folder = "pdfs/"
pdf_texts = extract_text_from_pdfs(pdf_folder)

# Combine extracted text from all PDFs
guideline_sentences = []
for filename, text in pdf_texts.items():
    guideline_sentences.extend(text.split("\n"))  # Split text into sentences

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