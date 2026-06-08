"""Tests for contacts.notes nested resource."""

import pytest
from unittest.mock import AsyncMock

from chatwoot.resources.contacts import AsyncContactsResource, ContactsResource
from chatwoot.types.note import Note


NOTE_PAYLOAD = {
    "id": 7,
    "content": "Followed up via email",
    "contact_id": 100,
    "user_id": 2,
    "account_id": 1,
    "created_at": "2024-01-01T10:00:00Z",
    "updated_at": "2024-01-01T10:00:00Z",
}

NOTES_LIST_PAYLOAD = [
    NOTE_PAYLOAD,
    {
        "id": 8,
        "content": "Second note",
        "contact_id": 100,
        "user_id": 2,
        "account_id": 1,
    },
]


def test_notes_list_returns_notes(mock_http):
    """Test listing notes returns a list of Note objects."""
    mock_http.get.return_value = NOTES_LIST_PAYLOAD

    resource = ContactsResource(mock_http)
    notes = resource.notes.list(account_id=1, contact_id=100)

    mock_http.get.assert_called_once_with("/api/v1/accounts/1/contacts/100/notes")
    assert isinstance(notes, list)
    assert len(notes) == 2
    assert all(isinstance(n, Note) for n in notes)
    assert notes[0].id == 7
    assert notes[0].content == "Followed up via email"


def test_notes_list_handles_payload_wrapper(mock_http):
    """Test listing notes handles payload-wrapped responses."""
    mock_http.get.return_value = {"payload": NOTES_LIST_PAYLOAD}

    resource = ContactsResource(mock_http)
    notes = resource.notes.list(account_id=1, contact_id=100)

    assert isinstance(notes, list)
    assert len(notes) == 2
    assert notes[1].id == 8


def test_notes_list_returns_empty_on_unexpected_shape(mock_http):
    """Test listing notes returns empty list when response is neither list nor payload."""
    mock_http.get.return_value = {}

    resource = ContactsResource(mock_http)
    notes = resource.notes.list(account_id=1, contact_id=100)

    assert notes == []


def test_notes_get_returns_single_note(mock_http):
    """Test fetching a single note returns a Note object."""
    mock_http.get.return_value = NOTE_PAYLOAD

    resource = ContactsResource(mock_http)
    note = resource.notes.get(account_id=1, contact_id=100, note_id=7)

    mock_http.get.assert_called_once_with("/api/v1/accounts/1/contacts/100/notes/7")
    assert isinstance(note, Note)
    assert note.id == 7
    assert note.content == "Followed up via email"


def test_notes_create_posts_wrapped_content(mock_http):
    """Test creating a note posts the wrapped note body."""
    mock_http.post.return_value = NOTE_PAYLOAD

    resource = ContactsResource(mock_http)
    note = resource.notes.create(
        account_id=1, contact_id=100, content="Followed up via email"
    )

    mock_http.post.assert_called_once_with(
        "/api/v1/accounts/1/contacts/100/notes",
        json={"note": {"content": "Followed up via email"}},
    )
    assert isinstance(note, Note)
    assert note.id == 7


def test_notes_update_patches_wrapped_content(mock_http):
    """Test updating a note patches the wrapped note body."""
    mock_http.patch.return_value = {**NOTE_PAYLOAD, "content": "Updated note text"}

    resource = ContactsResource(mock_http)
    note = resource.notes.update(
        account_id=1, contact_id=100, note_id=7, content="Updated note text"
    )

    mock_http.patch.assert_called_once_with(
        "/api/v1/accounts/1/contacts/100/notes/7",
        json={"note": {"content": "Updated note text"}},
    )
    assert isinstance(note, Note)
    assert note.content == "Updated note text"


def test_notes_delete_calls_delete_endpoint(mock_http):
    """Test deleting a note calls the delete endpoint."""
    resource = ContactsResource(mock_http)
    result = resource.notes.delete(account_id=1, contact_id=100, note_id=7)

    mock_http.delete.assert_called_once_with("/api/v1/accounts/1/contacts/100/notes/7")
    assert result is None


@pytest.mark.asyncio
async def test_async_notes_list(mock_async_http):
    """Test async listing notes."""
    mock_async_http.get = AsyncMock(return_value=NOTES_LIST_PAYLOAD)

    resource = AsyncContactsResource(mock_async_http)
    notes = await resource.notes.list(account_id=1, contact_id=100)

    mock_async_http.get.assert_called_once_with("/api/v1/accounts/1/contacts/100/notes")
    assert len(notes) == 2
    assert notes[0].id == 7


@pytest.mark.asyncio
async def test_async_notes_get(mock_async_http):
    """Test async fetching a single note."""
    mock_async_http.get = AsyncMock(return_value=NOTE_PAYLOAD)

    resource = AsyncContactsResource(mock_async_http)
    note = await resource.notes.get(account_id=1, contact_id=100, note_id=7)

    mock_async_http.get.assert_called_once_with(
        "/api/v1/accounts/1/contacts/100/notes/7"
    )
    assert isinstance(note, Note)
    assert note.id == 7


@pytest.mark.asyncio
async def test_async_notes_create(mock_async_http):
    """Test async creating a note."""
    mock_async_http.post = AsyncMock(return_value=NOTE_PAYLOAD)

    resource = AsyncContactsResource(mock_async_http)
    note = await resource.notes.create(
        account_id=1, contact_id=100, content="Followed up via email"
    )

    mock_async_http.post.assert_called_once_with(
        "/api/v1/accounts/1/contacts/100/notes",
        json={"note": {"content": "Followed up via email"}},
    )
    assert isinstance(note, Note)


@pytest.mark.asyncio
async def test_async_notes_update(mock_async_http):
    """Test async updating a note."""
    mock_async_http.patch = AsyncMock(
        return_value={**NOTE_PAYLOAD, "content": "Updated note text"}
    )

    resource = AsyncContactsResource(mock_async_http)
    note = await resource.notes.update(
        account_id=1, contact_id=100, note_id=7, content="Updated note text"
    )

    mock_async_http.patch.assert_called_once_with(
        "/api/v1/accounts/1/contacts/100/notes/7",
        json={"note": {"content": "Updated note text"}},
    )
    assert note.content == "Updated note text"


@pytest.mark.asyncio
async def test_async_notes_delete(mock_async_http):
    """Test async deleting a note."""
    mock_async_http.delete = AsyncMock(return_value=None)

    resource = AsyncContactsResource(mock_async_http)
    result = await resource.notes.delete(account_id=1, contact_id=100, note_id=7)

    mock_async_http.delete.assert_called_once_with(
        "/api/v1/accounts/1/contacts/100/notes/7"
    )
    assert result is None
