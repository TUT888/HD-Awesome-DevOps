import logging
import os
import time
import pytest
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient

from app.main import app
from app.db import Base, engine, SessionLocal, get_db
from app.models import Note

# Suppress noisy logs from SQLAlchemy/FastAPI during tests for cleaner output
logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
logging.getLogger("uvicorn.error").setLevel(logging.WARNING)
logging.getLogger("fastapi").setLevel(logging.WARNING)
logging.getLogger("app.main").setLevel(logging.WARNING)


@pytest.fixture(scope="session", autouse=True)
def setup_database_for_tests():
    """Set up test database with retry logic"""
    max_retries = 10
    retry_delay_seconds = 3

    for i in range(max_retries):
        try:
            logging.info(
                f"Notes Service Tests: Attempting to connect to PostgreSQL for test setup (attempt {i+1}/{max_retries})..."
            )

            # Explicitly drop all tables first to ensure a clean slate for the session
            Base.metadata.drop_all(bind=engine)
            logging.info(
                "Notes Service Tests: Successfully dropped all tables in PostgreSQL for test setup."
            )

            # Then create all tables required by the application
            Base.metadata.create_all(bind=engine)
            logging.info(
                "Notes Service Tests: Successfully created all tables in PostgreSQL for test setup."
            )
            break
        except OperationalError as e:
            logging.warning(
                f"Notes Service Tests: Test setup DB connection failed: {e}. Retrying in {retry_delay_seconds} seconds..."
            )
            time.sleep(retry_delay_seconds)
            if i == max_retries - 1:
                pytest.fail(
                    f"Could not connect to PostgreSQL for Product Service test setup after {max_retries} attempts: {e}"
                )
        except Exception as e:
            pytest.fail(
                f"Notes Service Tests: An unexpected error occurred during test DB setup: {e}",
                pytrace=True,
            )
    yield


@pytest.fixture(scope="function")
def db_session_for_test():
    """Provide isolated database session for each test"""
    connection = engine.connect()
    transaction = connection.begin()
    db = SessionLocal(bind=connection)

    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db

    try:
        yield db
    finally:
        transaction.rollback()
        db.close()
        connection.close()
        app.dependency_overrides.pop(get_db, None)


@pytest.fixture(scope="module")
def client():
    """
    Provides a TestClient for making HTTP requests to the FastAPI application.
    The TestClient automatically manages the app's lifespan events (startup/shutdown).
    """
    os.environ["AZURE_STORAGE_ACCOUNT_NAME"] = "testaccount"
    os.environ["AZURE_STORAGE_ACCOUNT_KEY"] = "testkey"
    os.environ["AZURE_STORAGE_CONTAINER_NAME"] = "test-images"
    os.environ["AZURE_SAS_TOKEN_EXPIRY_HOURS"] = "1"

    with TestClient(app) as test_client:
        yield test_client

    # Clean up environment variables after tests
    del os.environ["AZURE_STORAGE_ACCOUNT_NAME"]
    del os.environ["AZURE_STORAGE_ACCOUNT_KEY"]
    del os.environ["AZURE_STORAGE_CONTAINER_NAME"]
    del os.environ["AZURE_SAS_TOKEN_EXPIRY_HOURS"]
