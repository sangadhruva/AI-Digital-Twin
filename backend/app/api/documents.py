from pathlib import Path
from uuid import uuid4

from fastapi import (
    APIRouter,
    File,
    HTTPException,
    UploadFile,
)

from app.rag.chroma_service import (
    clear_collection,
    get_active_document_metadata,
    get_collection_count,
    store_document_chunks,
)
from app.rag.text_splitter import split_text
from app.services.document_parser import (
    SUPPORTED_EXTENSIONS,
    extract_text,
)

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)

BASE_DIR = Path(__file__).resolve().parents[2]
UPLOAD_DIR = BASE_DIR / "uploads"

UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

MAX_FILE_SIZE = 10 * 1024 * 1024


def clear_uploaded_files() -> None:
    for path in UPLOAD_DIR.iterdir():
        if path.is_file():
            path.unlink(
                missing_ok=True,
            )


@router.get("/status")
def get_document_status():
    stored_chunks = get_collection_count()
    active_document = get_active_document_metadata()

    if (
        stored_chunks == 0
        or active_document is None
        or not active_document.get("original_filename")
    ):
        return {
            "has_document": False,
            "original_filename": None,
            "stored_filename": None,
            "stored_chunks": 0,
        }

    return {
        "has_document": True,
        "original_filename": active_document[
            "original_filename"
        ],
        "stored_filename": active_document[
            "stored_filename"
        ],
        "stored_chunks": stored_chunks,
    }


@router.delete("/clear")
def clear_candidate_profile():
    try:
        clear_collection()
        clear_uploaded_files()

        return {
            "message": (
                "Candidate profile, uploaded files, "
                "and indexed document chunks were cleared."
            ),
            "stored_chunks": get_collection_count(),
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=(
                "Unable to clear candidate profile: "
                f"{error}"
            ),
        ) from error


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
):
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is required.",
        )

    original_filename = Path(
        file.filename,
    ).name

    extension = Path(
        original_filename,
    ).suffix.lower()

    if extension not in SUPPORTED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=(
                "Only PDF, DOCX, and TXT files "
                "are supported."
            ),
        )

    file_content = await file.read()

    if not file_content:
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is empty.",
        )

    if len(file_content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail=(
                "File is too large. "
                "Maximum size is 10 MB."
            ),
        )

    stored_filename = (
        f"{uuid4().hex}{extension}"
    )

    stored_path = (
        UPLOAD_DIR / stored_filename
    )

    try:
        stored_path.write_bytes(
            file_content,
        )

        extracted_text = extract_text(
            stored_path,
        )

        if not extracted_text:
            stored_path.unlink(
                missing_ok=True,
            )

            raise HTTPException(
                status_code=422,
                detail=(
                    "No readable text was found "
                    "in the document."
                ),
            )

        chunks = split_text(
            extracted_text,
        )

        if not chunks:
            stored_path.unlink(
                missing_ok=True,
            )

            raise HTTPException(
                status_code=422,
                detail=(
                    "The document could not be "
                    "divided into readable chunks."
                ),
            )

        # A single candidate profile is active at a time.
        clear_collection()

        # Remove previously uploaded candidate documents.
        for old_file in UPLOAD_DIR.iterdir():
            if (
                old_file.is_file()
                and old_file != stored_path
            ):
                old_file.unlink(
                    missing_ok=True,
                )

        stored_chunk_count = (
            store_document_chunks(
                chunks=chunks,
                original_filename=original_filename,
                stored_filename=stored_filename,
            )
        )

        return {
            "message": (
                "Previous candidate profile removed. "
                "New candidate document indexed successfully."
            ),
            "document": {
                "original_filename": original_filename,
                "stored_filename": stored_filename,
                "file_type": extension.removeprefix(
                    ".",
                ),
                "size_bytes": len(
                    file_content,
                ),
                "character_count": len(
                    extracted_text,
                ),
                "word_count": len(
                    extracted_text.split(),
                ),
                "chunk_count": stored_chunk_count,
                "vector_store_count": (
                    get_collection_count()
                ),
                "text_preview": extracted_text[:500],
            },
        }

    except HTTPException:
        raise

    except Exception as error:
        stored_path.unlink(
            missing_ok=True,
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Unable to process document: "
                f"{error}"
            ),
        ) from error

    finally:
        await file.close()