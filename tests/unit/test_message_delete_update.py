"""Tests for messages.delete and messages.update."""

import pytest
from unittest.mock import AsyncMock

from chatwoot.resources.messages import MessagesResource, AsyncMessagesResource
from chatwoot.types.message import Message


MESSAGE_PAYLOAD = {
    "id": 123,
    "content": "Hello",
    "message_type": "outgoing",
    "created_at": 1700000000,
    "conversation_id": 42,
}


# ---------------------------------------------------------------------------
# delete (sync)
# ---------------------------------------------------------------------------


def test_delete_includes_conversation_id_in_path(mock_http):
    """delete() must include conversation_id in the URL path."""
    mock_http.delete.return_value = {}

    resource = MessagesResource(mock_http)
    resource.delete(account_id=1, conversation_id=42, message_id=123)

    mock_http.delete.assert_called_once_with(
        "/api/v1/accounts/1/conversations/42/messages/123"
    )


# ---------------------------------------------------------------------------
# update (sync)
# ---------------------------------------------------------------------------


def test_update_sends_status(mock_http):
    """update() sends status in the request body."""
    mock_http.patch.return_value = MESSAGE_PAYLOAD

    resource = MessagesResource(mock_http)
    result = resource.update(
        account_id=1, conversation_id=42, message_id=123, status="delivered"
    )

    mock_http.patch.assert_called_once_with(
        "/api/v1/accounts/1/conversations/42/messages/123",
        json={"status": "delivered"},
    )
    assert isinstance(result, Message)
    assert result.id == 123


def test_update_sends_status_and_external_error(mock_http):
    """update() sends both status and external_error when provided."""
    mock_http.patch.return_value = MESSAGE_PAYLOAD

    resource = MessagesResource(mock_http)
    resource.update(
        account_id=1,
        conversation_id=42,
        message_id=123,
        status="failed",
        external_error="Gateway timeout",
    )

    mock_http.patch.assert_called_once_with(
        "/api/v1/accounts/1/conversations/42/messages/123",
        json={"status": "failed", "external_error": "Gateway timeout"},
    )


# ---------------------------------------------------------------------------
# async delete
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_async_delete_includes_conversation_id(mock_async_http):
    """Async delete() must include conversation_id in the URL path."""
    mock_async_http.delete = AsyncMock(return_value={})

    resource = AsyncMessagesResource(mock_async_http)
    await resource.delete(account_id=1, conversation_id=42, message_id=123)

    mock_async_http.delete.assert_called_once_with(
        "/api/v1/accounts/1/conversations/42/messages/123"
    )


# ---------------------------------------------------------------------------
# async update
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_async_update_sends_status(mock_async_http):
    """Async update() sends status in the request body."""
    mock_async_http.patch = AsyncMock(return_value=MESSAGE_PAYLOAD)

    resource = AsyncMessagesResource(mock_async_http)
    result = await resource.update(
        account_id=1, conversation_id=42, message_id=123, status="delivered"
    )

    mock_async_http.patch.assert_called_once_with(
        "/api/v1/accounts/1/conversations/42/messages/123",
        json={"status": "delivered"},
    )
    assert isinstance(result, Message)
    assert result.conversation_id == 42
