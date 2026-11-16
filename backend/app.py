import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore as Qdrant
from qdrant_client import QdrantClient
from supabase import create_client, Client

load_dotenv()

app = FastAPI(title="Serverless RAG API with Supabase", version="2.0")

# Setup Qdrant & Embeddings
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
COLLECTION_NAME = "pdf_rag_collection"

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
vector_store = Qdrant(
    client=client,
    collection_name=COLLECTION_NAME,
    embedding=embeddings,
)

# Setup Supabase Client
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Request schema
class QueryRequest(BaseModel):
    user_id: str
    question: str
    top_k: int = 3

@app.get("/")
def root():
    return {"status": "online", "message": "RAG API with Supabase is running"}

@app.post("/query")
def query_rag(request: QueryRequest):
    try:
        # 1. Perform similarity search in Qdrant
        results = vector_store.similarity_search(request.question, k=request.top_k)
        retrieved_chunks = [
            {"content": doc.page_content, "metadata": doc.metadata}
            for doc in results
        ]
        
        answer_text = "\n".join([doc["content"] for doc in retrieved_chunks])

        # 2. Save the chat history to Supabase
        supabase.table("chat_history").insert({
            "user_id": request.user_id,
            "question": request.question,
            "answer": answer_text
        }).execute()

        return {
            "user_id": request.user_id,
            "question": request.question,
            "results": retrieved_chunks,
            "status": "Saved to Supabase successfully!"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))