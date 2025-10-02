"""
Users Service API

FastAPI application for user authentication and management
"""

import logging
import sys
import time
from typing import List

from fastapi import (
    Depends,
    FastAPI,
    HTTPException,
    Query,
    status,
)
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session

from .db import Base, engine, get_db
from .models import User
from .schemas import UserCreate, UserResponse

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
    title="Users Service API",
    description="Manages users for multi-user note-taking application",
    version="1.0.0",
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
                f"Users Service: Attempting to connect to PostgreSQL and create tables (attempt {i+1}/{max_retries})..."
            )
            Base.metadata.create_all(bind=engine)
            logger.info(
                "Users Service: Successfully connected to PostgreSQL and ensured tables exist."
            )
            break  # Exit loop if successful
        except OperationalError as e:
            logger.warning(f"Users Service: Failed to connect to PostgreSQL: {e}")
            if i < max_retries - 1:
                logger.info(
                    f"Users Service: Retrying in {retry_delay_seconds} seconds..."
                )
                time.sleep(retry_delay_seconds)
            else:
                logger.critical(
                    f"Users Service: Failed to connect to PostgreSQL after {max_retries} attempts. Exiting application."
                )
                sys.exit(1)  # Critical failure: exit if DB connection is unavailable
        except Exception as e:
            logger.critical(
                f"Users Service: An unexpected error occurred during database startup: {e}",
                exc_info=True,
            )
            sys.exit(1)


# --- Root Endpoint ---
@app.get("/", status_code=status.HTTP_200_OK, summary="Root endpoint")
async def read_root():
    return {"message": "Welcome to the Users Service!"}


# --- Health Check Endpoint ---
@app.get("/health", status_code=status.HTTP_200_OK, summary="Health check")
async def health_check():
    return {"status": "ok", "service": "users-service"}


# --- CRUD Endpoints ---
# Create new user (Register)
# [POST] http://localhost:8001/users/
"""
{
    "username": "johndoe",
    "email": "john@example.com"
}
"""


@app.post(
    "/users/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user."""
    logger.info(f"Users Service: Creating user: {user.username}")

    # Check if username exists
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        logger.warning(f"Users Service: Username {user.username} already exists")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Username already exists"
        )

    # Check if email exists
    existing_email = db.query(User).filter(User.email == user.email).first()
    if existing_email:
        logger.warning(f"Users Service: Email {user.email} already exists")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email already exists"
        )

    try:
        db_user = User(username=user.username, email=user.email)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        logger.info(
            f"Users Service: User '{db_user.username}' (ID: {db_user.id}) created successfully."
        )
        return db_user
    except Exception as e:
        db.rollback()
        logger.error(f"Users Service: Error creating user: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not create user.",
        )


# Get user by ID
# [GET] http://localhost:8001/users/{user_id}
@app.get(
    "/users/{user_id}",
    response_model=UserResponse,
    summary="Get a single user by ID",
)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Retrieve a specific user by ID."""
    logger.info(f"Users Service: Fetching user with ID: {user_id}")
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        logger.warning(f"Users Service: User with ID {user_id} not found.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    logger.info(f"Users Service: Retrieved user with ID {user_id}")
    return user


# Get all users
# [GET] http://localhost:8001/users/
@app.get(
    "/users/",
    response_model=List[UserResponse],
    summary="Get all users",
)
def list_users(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
):
    """Retrieve all users."""
    logger.info(f"Users Service: Listing users with skip={skip}, limit={limit}")
    users = db.query(User).offset(skip).limit(limit).all()
    logger.info(f"Users Service: Retrieved {len(users)} users")
    return users
