import os
import requests
from dotenv import load_dotenv
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Qdrant
from qdrant_client import QdrantClient
from langchain.schema import Document
from langchain.chains import RetrievalQA
from langchain.llms import Ollama

load_dotenv()

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")
QDRANT_COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")
QDRANT_HOST = os.getenv("QDRANT_HOST")
QDRANT_PORT = int(os.getenv("QDRANT_PORT"))

embedder = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

retriever = Qdrant(
    client=client,
    collection_name=QDRANT_COLLECTION_NAME,
    embeddings=embedder
).as_retriever()

llm = Ollama(model=OLLAMA_MODEL, base_url=OLLAMA_BASE_URL)
qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

def insert_knowledge(text: str) -> int:
    chunks = [chunk.strip() for chunk in text.split("\n\n") if chunk.strip()]
    docs = [Document(page_content=chunk) for chunk in chunks]
    vectorstore = Qdrant(client=client, collection_name=QDRANT_COLLECTION_NAME, embeddings=embedder)
    vectorstore.add_documents(docs)
    return len(docs)

def validate_answer(question: str, answer: str) -> bool:
    validator_prompt = (
        f"以下はあるAIが『{question}』という質問に答えた内容です。\n"
        f"---\n{answer}\n---\n"
        "この回答は事実として問題がありますか？YESかNOで答えてください。"
    )
    result = llm(validator_prompt)
    return "NO" in result.upper()

def run_rag_pipeline(question: str) -> dict:
    answer = qa_chain.run(question)
    if validate_answer(question, answer):
        return {"question": question, "answer": answer}
    else:
        return {"question": question, "answer": None, "error": "Validation failed"}