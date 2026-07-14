from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.rag.chroma_service import (
    get_collection_count,
    search_document_chunks,
)
from app.services.rag_answer_service import answer_question


router = APIRouter(
    prefix="/rag",
    tags=["RAG"],
)


class SearchRequest(BaseModel):
    query: str = Field(
        min_length=2,
        description="Question or search query",
    )

    limit: int = Field(
        default=4,
        ge=1,
        le=10,
    )


class AskRequest(BaseModel):
    question: str = Field(
        min_length=2,
        description="Question for the AI Digital Twin",
    )

    limit: int = Field(
        default=4,
        ge=1,
        le=10,
    )


@router.get("/status")
def rag_status():
    return {
        "status": "ready",
        "stored_chunks": get_collection_count(),
    }


@router.post("/search")
def search_rag(payload: SearchRequest):
    stored_chunks = get_collection_count()

    if stored_chunks == 0:
        raise HTTPException(
            status_code=400,
            detail="No documents are indexed. Upload a document first.",
        )

    matches = search_document_chunks(
        query=payload.query,
        limit=payload.limit,
    )

    return {
        "query": payload.query,
        "match_count": len(matches),
        "matches": matches,
    }


@router.post("/ask")
def ask_digital_twin(payload: AskRequest):
    stored_chunks = get_collection_count()

    if stored_chunks == 0:
        raise HTTPException(
            status_code=400,
            detail="No documents are indexed. Upload a document first.",
        )

    result = answer_question(
        question=payload.question,
        limit=payload.limit,
    )

    return {
        "question": payload.question,
        "answer": result["answer"],
        "sources": result["sources"],
    }