import streamlit as st
import requests

st.set_page_config(page_title="PDF-RAG Chatbot", page_icon="🤖", layout="centered")

st.title("📚 Cloud-Based PDF-RAG Chatbot")
st.write("Chat with your document library backed by Qdrant and Supabase persistence.")

# Backend API URLs
FASTAPI_URL = "http://127.0.0.1:8000"

# Sidebar for configuration and document library
with st.sidebar:
    st.header("Session Settings")
    user_id = st.text_input("User ID", value="user_123")
    top_k = st.slider("Top Chunks to Retrieve", min_value=1, max_value=5, value=3)
    
    st.divider()
    
    st.header("📁 Document Library & Upload")
    uploaded_file = st.file_uploader("Upload a new PDF", type=["pdf"])
    
    if uploaded_file is not None:
        if st.button("Upload to Backend"):
            with st.spinner("Uploading and processing PDF..."):
                try:
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                    data = {"user_id": user_id}
                    response = requests.post(f"{FASTAPI_URL}/upload", files=files, data=data)
                    
                    if response.status_code == 200:
                        st.success("PDF uploaded and indexed successfully!")
                    else:
                        st.error(f"Upload failed: {response.text}")
                except Exception as e:
                    st.error(f"Connection error: {e}")

    st.subheader("Previously Uploaded PDFs")
    # Fetch document list from backend (assumes an endpoint like /documents exists)
    try:
        res = requests.get(f"{FASTAPI_URL}/documents?user_id={user_id}")
        if res.status_code == 200:
            docs = res.json().get("documents", [])
            if docs:
                for doc in docs:
                    st.text(f"📄 {doc}")
            else:
                st.info("No documents uploaded yet.")
        else:
            st.text("📄 sample.pdf (Default)")
    except Exception:
        st.text("📄 sample.pdf (Default)")

    if st.button("Clear Chat History"):
        st.session_state.messages = []

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display prior chat messages from history when app reruns
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input via chat input box
if prompt := st.chat_input("Ask something about your documents..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Call your FastAPI Backend query endpoint
    with st.chat_message("assistant"):
        with st.spinner("Thinking and searching documents..."):
            try:
                payload = {
                    "user_id": user_id,
                    "question": prompt,
                    "top_k": top_k
                }
                
                response = requests.post(f"{FASTAPI_URL}/query", json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    results = data.get("results", [])
                    if results:
                        answer_text = results[0].get("content", "No content found.")
                    else:
                        answer_text = "No matching information found in the documents."
                    
                    st.markdown(answer_text)
                    st.session_state.messages.append({"role": "assistant", "content": answer_text})
                else:
                    st.error(f"Backend error: {response.text}")
            except Exception as e:
                st.error(f"Could not connect to FastAPI backend: {e}")