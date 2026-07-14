from pathlib import Path
from uuid import uuid4

import chromadb
from chromadb.utils.embedding_functions import (
    SentenceTransformerEmbeddingFunction,
)

BASE_DIR = Path(__file__).resolve().parents[2]
CHROMA_PATH = BASE_DIR / "chroma_db"

client = chromadb.PersistentClient(
    path=str(CHROMA_PATH),
)

embedding_function = (
    SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2",
    )
)

COLLECTION_NAME = "digital_twin_documents"


def get_collection():
    return client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=embedding_function,
        metadata={
            "description": (
                "Candidate documents used by "
                "the Candidate Digital Twin"
            ),
        },
    )


collection = get_collection()


def clear_collection() -> None:
    global collection

    try:
        client.delete_collection(
            name=COLLECTION_NAME,
        )
    except Exception:
        # The collection may not exist yet.
        pass

    collection = get_collection()


def store_document_chunks(
    chunks: list[str],
    original_filename: str,
    stored_filename: str,
) -> int:
    if not chunks:
        return 0

    ids = [
        uuid4().hex
        for _ in chunks
    ]

    metadatas = [
        {
            "original_filename": original_filename,
            "stored_filename": stored_filename,
            "chunk_index": index,
        }
        for index in range(len(chunks))
    ]

    collection.add(
        ids=ids,
        documents=chunks,
        metadatas=metadatas,
    )

    return len(chunks)


def search_document_chunks(
    query: str,
    limit: int = 4,
) -> list[dict]:
    if not query.strip():
        return []

    total_chunks = collection.count()

    if total_chunks == 0:
        return []

    safe_limit = min(
        limit,
        total_chunks,
    )

    result = collection.query(
        query_texts=[query],
        n_results=safe_limit,
        include=[
            "documents",
            "metadatas",
            "distances",
        ],
    )

    documents = result.get(
        "documents",
        [[]],
    )[0]

    metadatas = result.get(
        "metadatas",
        [[]],
    )[0]

    distances = result.get(
        "distances",
        [[]],
    )[0]

    matches: list[dict] = []

    for document, metadata, distance in zip(
        documents,
        metadatas,
        distances,
    ):
        matches.append(
            {
                "text": document,
                "metadata": metadata,
                "distance": distance,
            }
        )

    return matches


def get_active_document_metadata() -> dict | None:
    if collection.count() == 0:
        return None

    result = collection.get(
        limit=1,
        include=["metadatas"],
    )

    metadatas = result.get(
        "metadatas",
        [],
    )

    if not metadatas:
        return None

    metadata = metadatas[0]

    if not metadata:
        return None

    return {
        "original_filename": metadata.get(
            "original_filename",
            "",
        ),
        "stored_filename": metadata.get(
            "stored_filename",
            "",
        ),
    }


def get_collection_count() -> int:
    return collection.count()