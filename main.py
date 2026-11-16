from backend.rag_engine import process_and_store_pdf

if __name__ == "__main__":
    print("🚀 Starting PDF ingestion pipeline...")
    process_and_store_pdf("sample.pdf")  # Adjust path to sample.pdf if needed
    print("✅ PDF successfully processed and stored in Qdrant!")