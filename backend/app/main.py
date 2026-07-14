from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.agent import router as agent_router
from app.api.documents import router as documents_router
from app.api.rag import router as rag_router


app = FastAPI(
    title="AI Digital Twin API",
    version="1.0.0",
    description="RAG and LangGraph-powered personal digital twin",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(documents_router)
app.include_router(rag_router)
app.include_router(agent_router)


@app.get("/")
def root():
    return {
        "status": "success",
        "message": "AI Digital Twin backend is running",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
    }