from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from pdf_parser import extract_text_from_pdf

model = SentenceTransformer("all-MiniLM-L6-v2")
pdf_text = extract_text_from_pdf("evicore_guidelines.pdf")
guideline_sentences = pdf_text.split("\n")

embeddings = model.encode(guideline_sentences)
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings))

def search_guideline(query):
    query_embedding = model.encode([query])
    _, result_indices = index.search(query_embedding, k=3)
    return [guideline_sentences[i] for i in result_indices[0]]