"""Tests for conversations.assign."""

import pytest
from unittest.mock import AsyncMock

from chatwoot.resources.conversations import (
    ConversationsResource,
    AsyncConversationsResource,
)
from chatwoot.types.agent import Agent
from chatwoot.types.team import Team


ENDPOINT = "/api/v1/accounts/1/conversations/42/assignments"

AGENT_RESPONSE = {
    "id": 10,
    "account_id": 1,
    "availability_status": "online",
    "auto_offline": True,
    "confirmed": True,
    "email": "agent@example.com",
    "provider": "email",
    "available_name": "Jane",
    "custom_attributes": {},
    "name": "Jane Doe",
    "role": "agent",
    "thumbnail": "https://example.com/avatar.png",
}

TEAM_RESPONSE = {
    "id": 7,
    "name": "Billing",
    "description": "Billing team",
    "allow_auto_assign": True,
    "account_id": 1,
    "is_member": True,
}


def test_assign_agent(mock_http):
    """Test assigning an agent returns an Agent."""
    mock_http.post.return_value = AGENT_RESPONSE

    resource = ConversationsResource(mock_http)
    agent = resource.assign(account_id=1, conversation_id=42, assignee_id=10)

    mock_http.post.assert_called_once_with(ENDPOINT, json={"assignee_id": 10})
    assert isinstance(agent, Agent)
    assert agent.id == 10
    assert agent.name == "Jane Doe"
    assert agent.role == "agent"


def test_assign_team(mock_http):
    """Test assigning a team returns a Team, not an Agent."""
    mock_http.post.return_value = TEAM_RESPONSE

    resource = ConversationsResource(mock_http)
    team = resource.assign(account_id=1, conversation_id=42, team_id=7)

    mock_http.post.assert_called_once_with(ENDPOINT, json={"team_id": 7})
    assert isinstance(team, Team)
    assert team.id == 7
    assert team.name == "Billing"


def test_unassign_agent(mock_http):
    """Test that None clears the assignment and returns None."""
    mock_http.post.return_value = None

    resource = ConversationsResource(mock_http)
    result = resource.assign(account_id=1, conversation_id=42, assignee_id=None)

    mock_http.post.assert_called_once_with(ENDPOINT, json={"assignee_id": None})
    assert result is None


def test_unassign_team(mock_http):
    """Test that an empty body for a cleared team assignment returns None."""
    mock_http.post.return_value = {}

    resource = ConversationsResource(mock_http)
    result = resource.assign(account_id=1, conversation_id=42, team_id=None)

    mock_http.post.assert_called_once_with(ENDPOINT, json={"team_id": None})
    assert result is None


def test_assign_without_target_is_rejected(mock_http):
    """Test that assigning nothing raises instead of calling the API."""
    resource = ConversationsResource(mock_http)

    with pytest.raises(ValueError, match="either assignee_id or team_id"):
        resource.assign(account_id=1, conversation_id=42)

    mock_http.post.assert_not_called()


def test_assign_both_targets_is_rejected(mock_http):
    """Test that passing both raises, since the API would ignore team_id."""
    resource = ConversationsResource(mock_http)

    with pytest.raises(ValueError, match="not both"):
        resource.assign(account_id=1, conversation_id=42, assignee_id=10, team_id=7)

    mock_http.post.assert_not_called()


def test_assign_none_agent_and_team_is_rejected(mock_http):
    """Test that a None assignee still counts as supplied."""
    resource = ConversationsResource(mock_http)

    with pytest.raises(ValueError, match="not both"):
        resource.assign(account_id=1, conversation_id=42, assignee_id=None, team_id=7)

    mock_http.post.assert_not_called()


# ---------------------------------------------------------------------------
# async variants
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_async_assign_agent(mock_async_http):
    """Test async assigning an agent."""
    mock_async_http.post = AsyncMock(return_value=AGENT_RESPONSE)

    resource = AsyncConversationsResource(mock_async_http)
    agent = await resource.assign(account_id=1, conversation_id=42, assignee_id=10)

    mock_async_http.post.assert_called_once_with(ENDPOINT, json={"assignee_id": 10})
    assert isinstance(agent, Agent)
    assert agent.id == 10


@pytest.mark.asyncio
async def test_async_assign_team(mock_async_http):
    """Test async assigning a team."""
    mock_async_http.post = AsyncMock(return_value=TEAM_RESPONSE)

    resource = AsyncConversationsResource(mock_async_http)
    team = await resource.assign(account_id=1, conversation_id=42, team_id=7)

    mock_async_http.post.assert_called_once_with(ENDPOINT, json={"team_id": 7})
    assert isinstance(team, Team)
    assert team.id == 7


@pytest.mark.asyncio
async def test_async_unassign(mock_async_http):
    """Test async clearing an assignment."""
    mock_async_http.post = AsyncMock(return_value=None)

    resource = AsyncConversationsResource(mock_async_http)
    result = await resource.assign(account_id=1, conversation_id=42, assignee_id=None)

    assert result is None


@pytest.mark.asyncio
async def test_async_assign_without_target_is_rejected(mock_async_http):
    """Test async assigning nothing raises before any request."""
    mock_async_http.post = AsyncMock()

    resource = AsyncConversationsResource(mock_async_http)
    with pytest.raises(ValueError, match="either assignee_id or team_id"):
        await resource.assign(account_id=1, conversation_id=42)

    mock_async_http.post.assert_not_called()
