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
async def query_guidelines(req: QueryRequest):
    # Extract input values
    health_plan = req.health_plan
    diagnosis = req.diagnosis
    procedure = req.procedure

    # Search the guidelines for relevant info
    guidelines = "\n".join(search_guideline(f"{diagnosis} {procedure}"))

    # Get the AI-generated response
    answer = ask_chatgpt(health_plan, diagnosis, procedure, guidelines)

    return {
        "health_plan": health_plan,
        "diagnosis": diagnosis,
        "procedure": procedure,
        "response": answer
    }
