"""Tests for conversation assignments (assign method)."""

import pytest
from unittest.mock import AsyncMock

from chatwoot.resources.conversations import ConversationsResource, AsyncConversationsResource
from chatwoot.types.conversation import Conversation


CONVERSATION_PAYLOAD = {
    "id": 42,
    "account_id": 1,
    "inbox_id": 3,
    "status": "open",
    "assignee_id": 10,
}


# ---------------------------------------------------------------------------
# assign to agent (sync)
# ---------------------------------------------------------------------------


def test_assign_to_agent(mock_http):
    """Assign calls POST on the /assignments endpoint with assignee_id."""
    mock_http.post.return_value = CONVERSATION_PAYLOAD

    resource = ConversationsResource(mock_http)
    result = resource.assign(account_id=1, conversation_id=42, assignee_id=10)

    mock_http.post.assert_called_once_with(
        "/api/v1/accounts/1/conversations/42/assignments",
        json={"assignee_id": 10},
    )
    assert isinstance(result, Conversation)
    assert result.id == 42
    assert result.assignee_id == 10


# ---------------------------------------------------------------------------
# assign to team (sync)
# ---------------------------------------------------------------------------


def test_assign_to_team(mock_http):
    """Assign calls POST on the /assignments endpoint with team_id."""
    mock_http.post.return_value = CONVERSATION_PAYLOAD

    resource = ConversationsResource(mock_http)
    result = resource.assign(account_id=1, conversation_id=42, team_id=5)

    mock_http.post.assert_called_once_with(
        "/api/v1/accounts/1/conversations/42/assignments",
        json={"team_id": 5},
    )
    assert isinstance(result, Conversation)


# ---------------------------------------------------------------------------
# assign does NOT hit the conversation update endpoint
# ---------------------------------------------------------------------------


def test_assign_does_not_call_patch(mock_http):
    """Assign must use POST /assignments, never PATCH /conversations."""
    mock_http.post.return_value = CONVERSATION_PAYLOAD

    resource = ConversationsResource(mock_http)
    resource.assign(account_id=1, conversation_id=42, assignee_id=10)

    mock_http.patch.assert_not_called()


# ---------------------------------------------------------------------------
# assign with both assignee_id and team_id
# ---------------------------------------------------------------------------


def test_assign_with_both_params(mock_http):
    """When both assignee_id and team_id are given, both are sent to the API."""
    mock_http.post.return_value = CONVERSATION_PAYLOAD

    resource = ConversationsResource(mock_http)
    resource.assign(account_id=1, conversation_id=42, assignee_id=10, team_id=5)

    mock_http.post.assert_called_once_with(
        "/api/v1/accounts/1/conversations/42/assignments",
        json={"assignee_id": 10, "team_id": 5},
    )


# ---------------------------------------------------------------------------
# assign with no params sends empty body
# ---------------------------------------------------------------------------


def test_assign_with_no_params(mock_http):
    """When neither assignee_id nor team_id is given, an empty body is sent."""
    mock_http.post.return_value = CONVERSATION_PAYLOAD

    resource = ConversationsResource(mock_http)
    resource.assign(account_id=1, conversation_id=42)

    mock_http.post.assert_called_once_with(
        "/api/v1/accounts/1/conversations/42/assignments",
        json={},
    )


# ---------------------------------------------------------------------------
# async variants
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_async_assign_to_agent(mock_async_http):
    """Async assign calls POST on the /assignments endpoint with assignee_id."""
    mock_async_http.post = AsyncMock(return_value=CONVERSATION_PAYLOAD)

    resource = AsyncConversationsResource(mock_async_http)
    result = await resource.assign(account_id=1, conversation_id=42, assignee_id=10)

    mock_async_http.post.assert_called_once_with(
        "/api/v1/accounts/1/conversations/42/assignments",
        json={"assignee_id": 10},
    )
    assert isinstance(result, Conversation)
    assert result.assignee_id == 10


@pytest.mark.asyncio
async def test_async_assign_to_team(mock_async_http):
    """Async assign calls POST on the /assignments endpoint with team_id."""
    mock_async_http.post = AsyncMock(return_value=CONVERSATION_PAYLOAD)

    resource = AsyncConversationsResource(mock_async_http)
    result = await resource.assign(account_id=1, conversation_id=42, team_id=5)

    mock_async_http.post.assert_called_once_with(
        "/api/v1/accounts/1/conversations/42/assignments",
        json={"team_id": 5},
    )
    assert isinstance(result, Conversation)


@pytest.mark.asyncio
async def test_async_assign_does_not_call_patch(mock_async_http):
    """Async assign must use POST /assignments, never PATCH /conversations."""
    mock_async_http.post = AsyncMock(return_value=CONVERSATION_PAYLOAD)

    resource = AsyncConversationsResource(mock_async_http)
    await resource.assign(account_id=1, conversation_id=42, assignee_id=10)

    mock_async_http.patch.assert_not_called()
