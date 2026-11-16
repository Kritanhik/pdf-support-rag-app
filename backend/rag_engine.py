import os
import sys

# Disable Chroma telemetry completely so it never tries to load gRPC/OpenTelemetry
os.environ["ANONYMIZED_TELEMETRY"] = "False"
os.environ["CHROMA_TELEMETRY_ENABLED"] = "False"

# Force Python to look in the root folder
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import chromadb
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

# 1. Load the PDF
pdf_path = "data/sample.pdf"
loader = PyPDFLoader(pdf_path)
pages = loader.load()

# 2. Split into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
docs = text_splitter.split_documents(pages)

# 3. Use native Chroma client directly
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="pdf_collection")

# 4. Add documents directly
texts = [doc.page_content for doc in docs]
metadatas = [doc.metadata for doc in docs]
ids = [str(i) for i in range(len(texts))]

collection.add(
    documents=texts,
    metadatas=metadatas,
    ids=ids
)

print(f"Successfully stored {len(texts)} chunks into native Chroma database!")