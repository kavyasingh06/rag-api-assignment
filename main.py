'''from fastapi import FastAPI, UploadFile, File, BackgroundTasks, Request, HTTPException
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.schemas import QueryRequest, QueryResponse
from app.ingestion import save_temp_file, process_document
from app.rag_engine import generate_answer

limiter = Limiter(key_func=get_remote_address)
app = FastAPI(title="Free RAG API")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/upload")
async def upload_document(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    if file.content_type not in ["application/pdf", "text/plain"]:
        raise HTTPException(400, "Only PDF or TXT allowed")
    
    file_path = save_temp_file(file)
    background_tasks.add_task(process_document, file_path)
    return {"message": "Processing in background"}

@app.post("/query", response_model=QueryResponse)
@limiter.limit("5/minute")
def ask(request: Request, query: QueryRequest):
    return generate_answer(query.question)'''
from fastapi import FastAPI, UploadFile, File, BackgroundTasks, Request, HTTPException
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.schemas import QueryRequest, QueryResponse
from app.ingestion import save_temp_file, process_document
from app.rag_engine import generate_answer

# Setup Rate Limiter
limiter = Limiter(key_func=get_remote_address)

# Initialize App
app = FastAPI(title="Free RAG API")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# --- NEW: Home Page Endpoint ---
@app.get("/")
def home():
    return {
        "message": "RAG System is running!",
        "instructions": "Go to /docs to upload files and ask questions."
    }

@app.post("/upload")
async def upload_document(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    # Validate file type
    if file.content_type not in ["application/pdf", "text/plain"]:
        raise HTTPException(status_code=400, detail="Only PDF or TXT files are allowed")
    
    # Save file and start background task
    file_path = save_temp_file(file)
    background_tasks.add_task(process_document, file_path)
    
    return {"message": f"File '{file.filename}' uploaded. Processing started in the background."}

@app.post("/query", response_model=QueryResponse)
@limiter.limit("5/minute")
def ask(request: Request, query: QueryRequest):
    return generate_answer(query.question)