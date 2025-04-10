# RAG-lite: Lightweight RAG System with FastAPI, LangChain, Ollama, and Qdrant

This project is a lightweight Retrieval-Augmented Generation (RAG) system using:

- [FastAPI](https://fastapi.tiangolo.com/) as the web framework
- [LangChain](https://www.langchain.com/) for chaining components
- [Ollama](https://ollama.ai/) to serve LLMs locally
- [Qdrant](https://qdrant.tech/) as the vector database
- [HuggingFace Embeddings](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)

---

## Features

- Lightweight and containerized
- Automatic RAG pipeline: embed → store → query → validate
- LLMs are served locally using Ollama
- Answer validation using a second model
- Optional startup initialization (create collection, load knowledge)

---

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/rag-lite.git
cd rag-lite

2. Set Environment Variables

Create a .env file based on the .env.example:

EMBEDDING_MODEL=all-MiniLM-L6-v2
OLLAMA_MODEL=cas/nous-hermes-2-mistral-7b-dpo
OLLAMA_BASE_URL=http://ollama:11434

QDRANT_HOST=qdrant
QDRANT_PORT=6333
QDRANT_VECTOR_SIZE=384
QDRANT_COLLECTION_NAME=mistral7b-rag

3. Build and Start the Containers

docker compose up --build



⸻

🧪 API Endpoints

POST /query

Query the RAG system with a natural language question.

{
  "question": "How is the Fukushima decommissioning progressing?"
}

POST /validate

Validate a generated answer using the validator model.

{
  "question": "How is the Fukushima decommissioning progressing?",
  "answer": "The reactor has already been completely removed."
}



⸻

📁 Project Structure

.
├── app/                      # FastAPI app
│   ├── main.py
│   ├── rag.py
│   └── ...
├── ollama/                   # Ollama container
│   ├── Dockerfile
│   └── entrypoint.sh
├── qdrant/                   # Qdrant container with entrypoint
│   ├── Dockerfile
│   └── entrypoint.sh
├── data/                     # Document store
│   └── docs.txt
├── .env
├── docker-compose.yml
└── README.md
