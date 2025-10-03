import pytest
from pydantic import ValidationError
from app.schemas import NoteCreate, NoteUpdate


def test_note_create_valid():
    note = NoteCreate(title="Test", content="Content", user_id=1)
    assert note.title == "Test"
    assert note.user_id == 1


def test_note_create_invalid_user_id():
    with pytest.raises(ValidationError):
        NoteCreate(title="Test", content="Content", user_id=-1)


def test_note_create_empty_title():
    with pytest.raises(ValidationError):
        NoteCreate(title="", content="Content", user_id=1)


def test_note_update_partial():
    update = NoteUpdate(title="New Title")
    assert update.title == "New Title"
    assert update.content is None
