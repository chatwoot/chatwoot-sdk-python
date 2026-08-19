"""Tests for conversations.update."""

import pytest
from unittest.mock import AsyncMock

from chatwoot.resources.conversations import (
    AsyncConversationsResource,
    ConversationsResource,
)
from chatwoot.types.conversation import Conversation


ENDPOINT = "/api/v1/accounts/1/conversations/42"

CONVERSATION_RESPONSE = {
    "id": 42,
    "account_id": 1,
    "inbox_id": 5,
    "status": "open",
    "priority": "high",
}


def test_update_priority(mock_http):
    """Test that priority reaches the API."""
    mock_http.patch.return_value = CONVERSATION_RESPONSE

    resource = ConversationsResource(mock_http)
    conversation = resource.update(account_id=1, conversation_id=42, priority="high")

    mock_http.patch.assert_called_once_with(ENDPOINT, json={"priority": "high"})
    assert isinstance(conversation, Conversation)
    assert conversation.priority == "high"


def test_update_extra_attribute_is_sent(mock_http):
    """Test that an unknown attribute still passes through kwargs."""
    mock_http.patch.return_value = CONVERSATION_RESPONSE

    resource = ConversationsResource(mock_http)
    resource.update(account_id=1, conversation_id=42, snoozed_until=123)

    mock_http.patch.assert_called_once_with(ENDPOINT, json={"snoozed_until": 123})


# ---------------------------------------------------------------------------
# async variants
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_async_update_priority(mock_async_http):
    """Test async update sends priority."""
    mock_async_http.patch = AsyncMock(return_value=CONVERSATION_RESPONSE)

    resource = AsyncConversationsResource(mock_async_http)
    conversation = await resource.update(
        account_id=1, conversation_id=42, priority="high"
    )

    mock_async_http.patch.assert_called_once_with(ENDPOINT, json={"priority": "high"})
    assert conversation.priority == "high"
