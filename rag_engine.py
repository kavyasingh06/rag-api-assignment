'''import os
import time
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from app.config import settings

def generate_answer(question: str):
    start_time = time.time()
    
    # 1. Check if index exists
    if not os.path.exists(settings.VECTOR_STORE_PATH):
        return {
            "answer": "No documents uploaded yet.",
            "sources": [],
            "latency": 0.0
        }

    # 2. Load Resources (Embeddings & Vector Store)
    embeddings = HuggingFaceEmbeddings(model_name=settings.EMBEDDING_MODEL)
    vector_store = FAISS.load_local(
        settings.VECTOR_STORE_PATH, 
        embeddings, 
        allow_dangerous_deserialization=True
    )
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})

    # 3. Define the LLM
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=0,
        google_api_key=settings.GOOGLE_API_KEY
    )

    # 4. Create the Prompt Template
    template = """Answer the question based only on the following context:
    {context}

    Question: {question}
    """
    prompt = PromptTemplate.from_template(template)

    # 5. Build the Chain (LCEL Style - No 'RetrievalQA' needed)
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    # 6. Run the Chain
    answer = rag_chain.invoke(question)
    
    # 7. Fetch sources manually for the response
    source_docs = retriever.invoke(question)
    sources = [doc.page_content[:150] + "..." for doc in source_docs]
    
    end_time = time.time()

    return {
        "answer": answer,
        "sources": sources,
        "latency": round(end_time - start_time, 2)
    }'''
import os
import time
import traceback
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from app.config import settings

def generate_answer(question: str):
    start_time = time.time()
    
    try:
        # 1. Check if index exists
        if not os.path.exists(settings.VECTOR_STORE_PATH):
            return {
                "answer": "No documents uploaded yet. Please upload a PDF first.",
                "sources": [],
                "latency": 0.0
            }

        # 2. Load Embeddings (This might be where it fails if model didn't download)
        print("Loading embeddings...")
        embeddings = HuggingFaceEmbeddings(model_name=settings.EMBEDDING_MODEL)
        
        # 3. Load Vector Store
        print("Loading vector store...")
        vector_store = FAISS.load_local(
            settings.VECTOR_STORE_PATH, 
            embeddings, 
            allow_dangerous_deserialization=True
        )
        retriever = vector_store.as_retriever(search_kwargs={"k": 3})

# 4. Define LLM
# 4. Define LLM
        print("Initializing Gemini...")
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",  # <--- UPDATED to match your list
            temperature=0,
            google_api_key=settings.GOOGLE_API_KEY
        )

        # 5. Define Prompt
        template = """Answer the question based only on the following context:
        {context}

        Question: {question}
        """
        prompt = PromptTemplate.from_template(template)

        # 6. Build Chain
        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)

        rag_chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )

        # 7. Run Chain
        print("Running chain...")
        answer = rag_chain.invoke(question)
        
        # 8. Get Sources
        source_docs = retriever.invoke(question)
        sources = [doc.page_content[:150] + "..." for doc in source_docs]
        
        end_time = time.time()

        return {
            "answer": answer,
            "sources": sources,
            "latency": round(end_time - start_time, 2)
        }

    except Exception as e:
        # Catch the crash and print it!
        error_msg = traceback.format_exc()
        print(error_msg) # Print to terminal
        return {
            "answer": f"SYSTEM ERROR: {str(e)}. CHECK TERMINAL FOR DETAILS.",
            "sources": [],
            "latency": 0.0
        }