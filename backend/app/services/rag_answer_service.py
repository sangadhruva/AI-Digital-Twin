import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq

from app.rag.chroma_service import search_document_chunks


load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "llama-3.1-8b-instant")

if not GROQ_API_KEY:
    raise RuntimeError(
        "GROQ_API_KEY is missing. Add it to backend/.env."
    )


llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model=MODEL_NAME,
    temperature=0.2,
)


def build_context(matches: list[dict]) -> str:
    context_parts: list[str] = []

    for index, match in enumerate(matches, start=1):
        source = match.get("metadata", {}).get(
            "original_filename",
            "Unknown document",
        )

        text = match.get("text", "").strip()

        context_parts.append(
            f"[Source {index}: {source}]\n{text}"
        )

    return "\n\n".join(context_parts)


def answer_question(
    question: str,
    limit: int = 4,
) -> dict:
    matches = search_document_chunks(
        query=question,
        limit=limit,
    )

    if not matches:
        return {
            "answer": (
                "I do not have enough information in the uploaded "
                "documents to answer that question."
            ),
            "sources": [],
            "matches": [],
        }

    context = build_context(matches)

    prompt = f"""
You are the personal AI Digital Twin of Sanga Dhruva.

Answer the user's question using ONLY the information provided in
the retrieved document context below.

Rules:
- Do not invent details.
- Do not use outside knowledge.
- If the context does not contain the answer, clearly say that the
  uploaded documents do not provide enough information.
- Answer in the first person when describing Sanga Dhruva.
- Keep the answer professional, clear, and suitable for recruiters.
- Do not mention vector databases, embeddings, retrieval, or chunks.
- Do not expose private contact information unless the user directly
  asks for contact information.

Retrieved context:
{context}

User question:
{question}

Answer:
"""

    response = llm.invoke(prompt)

    sources = sorted(
        {
            match.get("metadata", {}).get(
                "original_filename",
                "Unknown document",
            )
            for match in matches
        }
    )

    return {
        "answer": response.content.strip(),
        "sources": sources,
        "matches": matches,
    }