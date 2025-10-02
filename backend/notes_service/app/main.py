import logging
import sys, os, time
from typing import List, Optional

from fastapi import (
    Depends,
    FastAPI,
    HTTPException,
    Query,
    Response,
    status,
)
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session

from .db import Base, engine, get_db
from .models import Note
from .schemas import NoteCreate, NoteResponse, NoteUpdate

# --- Logging Configuration ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)

# Suppress noisy logs from third-party libraries for cleaner output
logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
logging.getLogger("uvicorn.error").setLevel(logging.INFO)

# --- FastAPI Application Setup ---
app = FastAPI(
    title="Notes Service API",
    description="Manages notes for multi-user note-taking application",
    version="1.0.0",
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Use specific origins in Notesion
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Startup Event ---
@app.on_event("startup")
async def startup_event():
    max_retries = 10
    retry_delay_seconds = 5
    for i in range(max_retries):
        try:
            logger.info(
                f"Notes Service: Attempting to connect to PostgreSQL and create tables (attempt {i+1}/{max_retries})..."
            )
            Base.metadata.create_all(bind=engine)
            logger.info(
                "Notes Service: Successfully connected to PostgreSQL and ensured tables exist."
            )
            break  # Exit loop if successful
        except OperationalError as e:
            logger.warning(f"Notes Service: Failed to connect to PostgreSQL: {e}")
            if i < max_retries - 1:
                logger.info(
                    f"Notes Service: Retrying in {retry_delay_seconds} seconds..."
                )
                time.sleep(retry_delay_seconds)
            else:
                logger.critical(
                    f"Notes Service: Failed to connect to PostgreSQL after {max_retries} attempts. Exiting application."
                )
                sys.exit(1)  # Critical failure: exit if DB connection is unavailable
        except Exception as e:
            logger.critical(
                f"Notes Service: An unexpected error occurred during database startup: {e}",
                exc_info=True,
            )
            sys.exit(1)


# --- Root Endpoint ---
@app.get("/", status_code=status.HTTP_200_OK, summary="Root endpoint")
async def read_root():
    return {"message": "Welcome to the Notes Service!"}


# --- Health Check Endpoint ---
@app.get("/health", status_code=status.HTTP_200_OK, summary="Health check")
async def health_check():
    return {"status": "ok", "service": "notes-service"}


# --- CRUD Endpoints ---
# Create new note
# [POST] http://localhost:8000/notes/
"""
{
    "title": "Sample Note",
    "content": "Sample ID",
    "user_id": 1
}
"""


@app.post(
    "/notes/",
    response_model=NoteResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new note",
)
async def create_note(note: NoteCreate, db: Session = Depends(get_db)):
    """Create a new note"""
    logger.info(f"Notes Service: Creating note: {note.title}")
    try:
        db_note = Note(**note.model_dump())
        db.add(db_note)
        db.commit()
        db.refresh(db_note)
        logger.info(
            f"Notes Service: Note '{db_note.title}' (ID: {db_note.id}) created successfully."
        )
        return db_note
    except Exception as e:
        db.rollback()
        logger.error(f"Notes Service: Error creating note: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not create note.",
        )


# Get all note for specific user
# [GET] http://localhost:8000/notes/?user_id={user_id}
@app.get(
    "/notes/",
    response_model=List[NoteResponse],
    summary="Get all notes for a user",
)
def list_notes(
    user_id: int = Query(..., description="User ID to fetch notes for"),
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
):
    """Retrieve all notes for a specific user"""
    logger.info(f"Notes Service: Listing notes for user {user_id}")
    notes = (
        db.query(Note).filter(Note.user_id == user_id).offset(skip).limit(limit).all()
    )
    logger.info(f"Notes Service: Retrieved {len(notes)} notes for user {user_id}")
    return notes


# Get specific note by note_id
# [GET] http://localhost:8000/notes/{note_id}
@app.get(
    "/notes/{note_id}",
    response_model=NoteResponse,
    summary="Get a single note by ID",
)
def get_note(note_id: int, db: Session = Depends(get_db)):
    """Retrieve a specific note by ID"""
    logger.info(f"Notes Service: Fetching note with ID: {note_id}")
    note = db.query(Note).filter(Note.id == note_id).first()

    if not note:
        logger.warning(f"Notes Service: Note with ID {note_id} not found.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Note not found"
        )

    logger.info(f"Notes Service: Retrieved note with ID {note_id}")
    return note


# Update specific note by note_id
# [PUT] http://localhost:8000/notes/{note_id}
"""
{
    "title": "Sample Note",
    "content": "Sample Updated Content"
}
"""


@app.put(
    "/notes/{note_id}",
    response_model=NoteResponse,
    summary="Update a note by ID",
)
async def update_note(note_id: int, note: NoteUpdate, db: Session = Depends(get_db)):
    """Update an existing note"""
    logger.info(f"Notes Service: Updating note with ID: {note_id}")
    db_note = db.query(Note).filter(Note.id == note_id).first()

    if not db_note:
        logger.warning(f"Notes Service: Note with ID {note_id} not found for update.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Note not found"
        )

    update_data = note.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_note, key, value)

    try:
        db.add(db_note)
        db.commit()
        db.refresh(db_note)
        logger.info(f"Notes Service: Note {note_id} updated successfully.")
        return db_note
    except Exception as e:
        db.rollback()
        logger.error(
            f"Notes Service: Error updating note {note_id}: {e}", exc_info=True
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not update note.",
        )


# Delete specific note by note_id
# [DELETE] http://localhost:8000/notes/{note_id}
@app.delete(
    "/notes/{note_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a note by ID",
)
def delete_note(note_id: int, db: Session = Depends(get_db)):
    """Delete a note"""
    logger.info(f"Notes Service: Attempting to delete note with ID: {note_id}")
    note = db.query(Note).filter(Note.id == note_id).first()

    if not note:
        logger.warning(f"Notes Service: Note with ID {note_id} not found for deletion.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Note not found"
        )

    try:
        db.delete(note)
        db.commit()
        logger.info(f"Notes Service: Note {note_id} deleted successfully.")
    except Exception as e:
        db.rollback()
        logger.error(
            f"Notes Service: Error deleting note {note_id}: {e}", exc_info=True
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not delete note.",
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)
