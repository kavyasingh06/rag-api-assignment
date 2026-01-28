# RAG-Based Question Answering API

A lightweight, asynchronous Retrieval-Augmented Generation (RAG) API built with FastAPI, FAISS, and Google Gemini. It allows users to upload PDF/TXT documents and ask questions based on those documents.

## 🏗️ Architecture
The system uses an asynchronous pipeline for document ingestion and a synchronous pipeline for retrieval and generation.

```mermaid
graph TD
    A[User] -->|POST /upload| B(FastAPI Endpoint)
    B -->|Trigger| C{Background Task}
    B -->|Return 202| A
    C -->|Parse| D[PDF/Text Loader]
    D -->|Chunk| E[Recursive Splitter]
    E -->|Embed| F[HuggingFace Embeddings]
    F -->|Store| G[(FAISS Vector DB)]
    
    A -->|POST /query| H(FastAPI Endpoint)
    H -->|Embed Query| F
    H -->|Search Top-K| G
    G -->|Retrieve Context| I[LLM Context]
    I -->|Generate| J[Google Gemini 2.5 Flash]
    J -->|Response| A
📊 Mandatory Explanations & Design Decisions
1. Chunking Strategy
Choice: Chunk Size: 500 characters | Overlap: 50 characters Rationale: We used RecursiveCharacterTextSplitter. A size of 500 characters was chosen because the embedding model (all-MiniLM-L6-v2) performs best with concise semantic units (typically 128-256 tokens). Larger chunks risk diluting the semantic meaning, while smaller chunks might lose context. The 50-character overlap ensures that sentences split at boundaries preserve their meaning across chunks.

2. Retrieval Failure Case
Observation: When asking "Summarize the entire document", the system provides an incomplete summary. Reason: This is a standard limitation of RAG. The retriever fetches the top k=3 chunks based on vector similarity. It does not pass the entire document to the LLM. Therefore, the LLM generates a summary based only on the 3 retrieved paragraphs, ignoring the rest of the file.

3. Metric Tracked
Metric: End-to-End Latency We track the time taken from receiving the query to returning the answer. This is returned in the JSON response as latency.

Average observed latency: ~1.5 seconds (mostly dependent on the Gemini API response time).

🚀 Features
Document Ingestion: Supports PDF and TXT formats.

Background Processing: Uploads return immediately while processing happens in the background.

Local Vector Store: Uses FAISS (CPU) for zero-cost, fast retrieval.

LLM Integration: Powered by Google Gemini 2.5 Flash.

Rate Limiting: Limited to 5 requests/minute per IP.

Observability: Returns latency and source chunks with every response.

🛠️ Setup Instructions
Clone the repository:

Bash
git clone <YOUR_GITHUB_REPO_LINK_HERE>
cd rag-app
Install dependencies:

Bash
pip install -r requirements.txt
Set up Environment Variables: Create a .env file in the root directory:

Ini, TOML
GOOGLE_API_KEY=your_google_api_key_here
Run the Server:

Bash
uvicorn app.main:app --reload
Access the API: Open your browser to: http://127.0.0.1:8000/docs
