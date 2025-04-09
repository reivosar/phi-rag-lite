from fastapi import FastAPI, Request

import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from rag import run_rag_pipeline, validate_answer, insert_knowledge

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "RAG + Validation API is running"}

@app.post("/query")
async def query(request: Request):
    body = await request.json()
    question = body.get("question", "")
    if not question:
        return {"error": "No question provided"}
    
    response = run_rag_pipeline(question)
    return response

@app.post("/validate")
async def validate(request: Request):
    body = await request.json()
    question = body.get("question", "")
    answer = body.get("answer", "")

    if not question or not answer:
        return {"error": "question and answer are both required"}

    is_valid = validate_answer(question, answer)
    return {
        "question": question,
        "answer": answer,
        "valid": is_valid
    }

@app.post("/ingest")
async def ingest_knowledge(request: Request):
    body = await request.json()
    text = body.get("text", "")
    if not text:
        return {"error": "No text provided"}
    
    num_inserted = insert_knowledge(text)
    return {"status": "ok", "documents_inserted": num_inserted}