# RAG-Based Question Answering API

A lightweight, asynchronous Retrieval-Augmented Generation (RAG) API built with FastAPI, FAISS, and Google Gemini. It allows users to upload PDF/TXT documents and ask questions based on those documents.

## 🏗️ Architecture
The system uses an asynchronous pipeline for document ingestion and a synchronous pipeline for retrieval and generation.

![Architecture Diagram](https://mermaid.ink/img/pako:eNqVkltv2jAQx7_KyMepEkgIb30ASlVbtQ9tH6Y-TAy4xKXYyDalqvjdd06AlE2l9iHxuXP8__vO8R1cJTMkCTM8K94WvMzpAzA0y0teFLwoyrIqC76-vOTF-xKjWfG6rAv6-v6OF29L_l5UPEeS7O9f4A08wWc0T0jCjCgQ-Ea2tL0nK8Q4w2tKk6e11m7-5Y-0QjJmeEYi6yDGC3oFf0h8iWcIEsR4Qd18O8Yf42cM4xmmG3sH8QZp3s3b3v0j3sDtfY5nJGI0I2F83N_dO4h3SPMBiRmO8W8QO3XyX07I5pS01q21z2_w0lqf3_C1tQ6_4Y-t9fwNf26th294aa21b_hra619w99a6-EbvrHWwzd8a621b_jOWmve8L211rzhB2u9e8MP1nr4hh-ttfYNP1rr3Rt-stbaN_xkrXdveG2ttW94ba13b3htrYdv-Nlaa9_ws7XeveFna619w8_WeveG19Y6_IbX1nr3htfWeviGf7TWu3f8_x9t21_4x8_W4f_4z1qH_4O_4xXj5GDrp0e-P5lq89gMv242y816tVpvhvVqN13v1uP1fNccpvt1c5wO-8N4N-2mw_V4uB52u_V-s9vt7g6Tw_S43W4?type=png)

## 📊 Mandatory Explanations & Design Decisions

### 1. Chunking Strategy
**Choice:** Chunk Size: 500 characters | Overlap: 50 characters
**Rationale:** We used `RecursiveCharacterTextSplitter`. A size of 500 characters was chosen because the embedding model (`all-MiniLM-L6-v2`) performs best with concise semantic units (typically 128-256 tokens). Larger chunks risk diluting the semantic meaning, while smaller chunks might lose context. The 50-character overlap ensures that sentences split at boundaries preserve their meaning across chunks.

### 2. Retrieval Failure Case
**Observation:**
When asking "Summarize the entire document", the system provides an incomplete summary.
**Reason:**
This is a standard limitation of RAG. The retriever fetches the top `k=3` chunks based on vector similarity. It does not pass the *entire* document to the LLM. Therefore, the LLM generates a summary based only on the 3 retrieved paragraphs, ignoring the rest of the file.

### 3. Metric Tracked
**Metric:** **End-to-End Latency**
We track the time taken from receiving the query to returning the answer. This is returned in the JSON response as `latency`.
* *Average observed latency:* ~1.5 seconds (mostly dependent on the Gemini API response time).

## 🚀 Features
* **Document Ingestion:** Supports PDF and TXT formats.
* **Background Processing:** Uploads return immediately while processing happens in the background.
* **Local Vector Store:** Uses FAISS (CPU) for zero-cost, fast retrieval.
* **LLM Integration:** Powered by Google Gemini 2.5 Flash.
* **Rate Limiting:** Limited to 5 requests/minute per IP.
* **Observability:** Returns latency and source chunks with every response.

## 🛠️ Setup Instructions

1.  **Clone the repository:**
    ```bash
    git clone <YOUR_GITHUB_REPO_LINK_HERE>
    cd rag-app
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up Environment Variables:**
    Create a `.env` file in the root directory:
    ```ini
    GOOGLE_API_KEY=your_google_api_key_here
    ```

4.  **Run the Server:**
    ```bash
    uvicorn app.main:app --reload
    ```

5.  **Access the API:**
    Open your browser to: `http://127.0.0.1:8000/docs`


