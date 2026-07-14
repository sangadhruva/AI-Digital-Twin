from typing import TypedDict

from langgraph.graph import END, StateGraph

from app.rag.chroma_service import search_document_chunks
from app.services.rag_answer_service import build_context, llm


class DigitalTwinState(TypedDict):
    question: str
    intent: str
    matches: list[dict]
    context: str
    has_context: bool
    answer: str
    sources: list[str]


def classify_question(state: DigitalTwinState) -> dict:
    question = state["question"].lower()

    if any(
        keyword in question
        for keyword in [
            "skill",
            "programming",
            "technology",
            "language",
            "framework",
        ]
    ):
        intent = "skills"

    elif any(
        keyword in question
        for keyword in [
            "education",
            "degree",
            "college",
            "cgpa",
            "school",
        ]
    ):
        intent = "education"

    elif any(
        keyword in question
        for keyword in [
            "experience",
            "internship",
            "worked",
            "project",
        ]
    ):
        intent = "experience"

    elif any(
        keyword in question
        for keyword in [
            "certificate",
            "certification",
            "achievement",
        ]
    ):
        intent = "certifications"

    elif any(
        keyword in question
        for keyword in [
            "contact",
            "email",
            "phone",
            "linkedin",
        ]
    ):
        intent = "contact"

    else:
        intent = "general"

    return {
        "intent": intent,
    }


def retrieve_context(state: DigitalTwinState) -> dict:
    matches = search_document_chunks(
        query=state["question"],
        limit=4,
    )

    context = build_context(matches)

    return {
        "matches": matches,
        "context": context,
        "has_context": bool(context.strip()),
    }


def route_after_retrieval(state: DigitalTwinState) -> str:
    if state["has_context"]:
        return "generate_answer"

    return "fallback_answer"


def generate_answer(state: DigitalTwinState) -> dict:
    prompt = f"""
You are the personal AI Digital Twin of Sanga Dhruva.

Answer the user's question using only the retrieved document context.

Rules:
- Do not invent facts.
- Do not use outside knowledge.
- Answer in the first person when describing Sanga Dhruva.
- Keep the answer professional and suitable for recruiters.
- Do not mention retrieval, chunks, embeddings, or vector databases.
- If the context is insufficient, clearly say so.
- Do not reveal private contact details unless the user directly asks.

Detected question category:
{state["intent"]}

Retrieved context:
{state["context"]}

User question:
{state["question"]}

Answer:
"""

    response = llm.invoke(prompt)

    sources = sorted(
        {
            str(
                (match.get("metadata") or {}).get(
                    "original_filename",
                    "Unknown document",
                )
            )
            for match in state["matches"]
        }
    )

    return {
        "answer": str(response.content).strip(),
        "sources": sources,
    }


def fallback_answer(_: DigitalTwinState) -> dict:
    return {
        "answer": (
            "I do not have enough information in my uploaded documents "
            "to answer that question."
        ),
        "sources": [],
    }


graph_builder = StateGraph(DigitalTwinState)

graph_builder.add_node(
    "classify_question",
    classify_question,
)

graph_builder.add_node(
    "retrieve_context",
    retrieve_context,
)

graph_builder.add_node(
    "generate_answer",
    generate_answer,
)

graph_builder.add_node(
    "fallback_answer",
    fallback_answer,
)

graph_builder.set_entry_point("classify_question")

graph_builder.add_edge(
    "classify_question",
    "retrieve_context",
)

graph_builder.add_conditional_edges(
    "retrieve_context",
    route_after_retrieval,
    {
        "generate_answer": "generate_answer",
        "fallback_answer": "fallback_answer",
    },
)

graph_builder.add_edge(
    "generate_answer",
    END,
)

graph_builder.add_edge(
    "fallback_answer",
    END,
)

digital_twin_graph = graph_builder.compile()


def run_digital_twin_agent(question: str) -> dict:
    result = digital_twin_graph.invoke(
        {
            "question": question,
            "intent": "",
            "matches": [],
            "context": "",
            "has_context": False,
            "answer": "",
            "sources": [],
        }
    )

    return {
        "question": result["question"],
        "intent": result["intent"],
        "answer": result["answer"],
        "sources": result["sources"],
        "retrieved_chunks": len(result["matches"]),
    }