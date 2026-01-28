# Project Report & Design Decisions

## 1. Chunking Strategy
**Choice:** Chunk Size: 500 characters | Overlap: 50 characters
**Rationale:** I chose a chunk size of 500 characters because the embedding model (`all-MiniLM-L6-v2`) performs best with concise semantic units (typically 128-256 tokens). 
* **Size:** Larger chunks (1000+) often dilute the semantic meaning, making vector search less accurate. 
* **Overlap:** The 50-character overlap ensures that sentences split at the boundaries of chunks are not lost, preserving context for the retriever.

## 2. Retrieval Failure Case
**Observation:**
When asking "Summarize the entire document," the system provides an incomplete or generic summary.
**Reason:**
This is a fundamental limitation of the RAG (Retrieval-Augmented Generation) architecture. The retriever fetches the top `k=3` chunks based on similarity to the word "summarize". It does not pass the *entire* document to the LLM. Therefore, the LLM generates a summary based only on those 3 specific paragraphs, ignoring the rest of the file.

## 3. Metrics Tracked
**Metric: End-to-End Latency**
**How:** I used Python's `time` module to calculate `start_time` before the chain runs and `end_time` after the response is generated.
**Value:** This metric is returned in the API response JSON (`"latency": 1.23`). 
**Why:** Latency is critical for user experience. Tracking this helps identify if the bottleneck is the vector search (FAISS) or the LLM generation (Google Gemini).