from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from generate_module import generate_answer

app = FastAPI(title="Secure RAG System", description="HR Handbook Q&A with security guardrails and evaluation")

# ---- Request/Response schemas ----
class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    question: str
    answer: str
    sources_used: int

# ---- Endpoints ----
@app.get("/")
def serve_frontend():
    return FileResponse("index.html")

@app.post("/ask", response_model=QueryResponse)
def ask_question(request: QueryRequest):
    answer, chunks = generate_answer(request.question)
    return QueryResponse(
        question=request.question,
        answer=answer,
        sources_used=len(chunks)
    )