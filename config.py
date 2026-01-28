import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    VECTOR_STORE_PATH = "data/faiss_index"
    EMBEDDING_MODEL = "all-MiniLM-L6-v2" # Free, fast, local model
    CHUNK_SIZE = 500
    CHUNK_OVERLAP = 50

settings = Settings()