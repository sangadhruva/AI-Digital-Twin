from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.agents.digital_twin_agent import (
    run_digital_twin_agent,
)
from app.rag.chroma_service import (
    get_collection_count,
)


router = APIRouter(
    prefix="/agent",
    tags=["LangGraph Agent"],
)


class AgentQuestionRequest(BaseModel):
    question: str = Field(
        min_length=2,
        description="Question about the indexed candidate",
    )


@router.post("/ask")
def ask_agent(
    payload: AgentQuestionRequest,
):
    stored_chunks = get_collection_count()

    if stored_chunks == 0:
        raise HTTPException(
            status_code=400,
            detail=(
                "No candidate document is indexed. "
                "Upload a document before asking questions."
            ),
        )

    return run_digital_twin_agent(
        payload.question,
    )