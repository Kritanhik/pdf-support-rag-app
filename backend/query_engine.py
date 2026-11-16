import os
import sys

# Disable telemetry flags
os.environ["ANONYMIZED_TELEMETRY"] = "False"
os.environ["CHROMA_TELEMETRY_ENABLED"] = "False"

# Force Python to locate the root-level grpc mock
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import chromadb
from dotenv import load_dotenv

load_dotenv()

# 1. Initialize the native Chroma persistent client
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="pdf_collection")

# 2. Define a test query
query_text = "What is the main topic of the document?"  # Change this to your test question

# 3. Query the collection directly
results = collection.query(
    query_texts=[query_text],
    n_results=3
)

print(f"\n--- Search Results for: '{query_text}' ---\n")
for i, (document, metadata) in enumerate(zip(results['documents'][0], results['metadatas'][0])):
    print(f"Result {i+1} (Source: {metadata.get('source', 'Unknown')} - Page {metadata.get('page', 'Unknown')}):")
    print(f"{document}\n" + "-"*40)