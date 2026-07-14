import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.agent import router as agent_router
from app.api.documents import router as documents_router
from app.api.rag import router as rag_router


def get_allowed_origins() -> list[str]:
    configured_origins = os.getenv(
        "CORS_ORIGINS",
        (
            "http://localhost:5173,"
            "http://127.0.0.1:5173"
        ),
    )

    return [
        origin.strip()
        for origin in configured_origins.split(",")
        if origin.strip()
    ]


app = FastAPI(
    title="Candidate Digital Twin API",
    version="1.0.0",
    description=(
        "RAG and LangGraph-powered recruiter assistant"
    ),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_allowed_origins(),
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
        "message": "Candidate Digital Twin backend is running",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
    }