import os
import shutil
from fastapi import UploadFile
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from app.config import settings

def save_temp_file(file: UploadFile, temp_dir="temp") -> str:
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    file_path = os.path.join(temp_dir, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return file_path

def process_document(file_path: str):
    try:
        # 1. Load Document
        if file_path.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
        elif file_path.endswith(".txt"):
            loader = TextLoader(file_path)
        else:
            return
        
        documents = loader.load()

        # 2. Chunk Text
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
            separators=["\n\n", "\n", " ", ""]
        )
        chunks = text_splitter.split_documents(documents)

        # 3. Embed & Store (Using Local CPU Embeddings)
        # This downloads a small model (80MB) once and runs locally
        embeddings = HuggingFaceEmbeddings(model_name=settings.EMBEDDING_MODEL)
        
        if os.path.exists(settings.VECTOR_STORE_PATH):
            try:
                vector_store = FAISS.load_local(
                    settings.VECTOR_STORE_PATH, 
                    embeddings, 
                    allow_dangerous_deserialization=True
                )
                vector_store.add_documents(chunks)
            except:
                vector_store = FAISS.from_documents(chunks, embeddings)
        else:
            vector_store = FAISS.from_documents(chunks, embeddings)

        vector_store.save_local(settings.VECTOR_STORE_PATH)
        print(f"Processed: {file_path}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)