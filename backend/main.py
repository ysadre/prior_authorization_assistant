from fastapi import FastAPI
from pydantic import BaseModel
from vector_search import search_guideline
from gpt_query import ask_chatgpt

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # ✅ Only allow requests from React frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request Model for API Input
class QueryRequest(BaseModel):
    health_plan: str
    diagnosis: str
    procedure: str

def clean_markdown(text):
    # Remove markdown headers (####, ###, ##, #)
    text = re.sub(r"^#+\s*", "", text, flags=re.MULTILINE)

    # Convert **bold text** to actual <strong> tags
    text = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", text)

    return text
    
@app.post("/api/query")
async def query_guidelines(request: QueryRequest):
    """Process the PA request and fetch relevant guidelines"""

    # Get relevant text and page numbers from the PDF
    guidelines, source_pages = search_guideline(request.diagnosis, request.procedure)

    # If no relevant guidelines are found, return a default response
    if not guidelines:
        return {
            "response": f"No specific guidelines found for {request.procedure} related to {request.diagnosis}. Please check payer policies.",
            "pages": []
        }

    # Extract the most relevant section for display
    source_text = "\n".join(guidelines[:2])  # Take only the most relevant 2 sections

    # Generate AI response using extracted guidelines
    answer = ask_chatgpt(
        request.health_plan, request.diagnosis, request.procedure, guidelines, source_text, source_pages
    )

    return {
        "response": answer,
        "pages": source_pages  # Return relevant PDF pages
    }
