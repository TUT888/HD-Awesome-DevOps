from app.models import Note


def test_note_repr():
    note = Note(id=1, title="Test", content="Content", user_id=1)
    repr_str = repr(note)
    assert "Note" in repr_str
    assert "id=1" in repr_str
