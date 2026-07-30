"""Tests for inboxes.agents.update and inboxes.agents.remove."""

import pytest
from unittest.mock import AsyncMock

from chatwoot.resources.inboxes import InboxMembersResource, AsyncInboxMembersResource
from chatwoot.types.agent import Agent


AGENT_PAYLOAD = [
    {
        "id": 10,
        "name": "Alice",
        "email": "alice@example.com",
        "role": "agent",
        "availability_status": "online",
        "confirmed": True,
        "account_id": 1,
    },
]


# ---------------------------------------------------------------------------
# update (PATCH — replaces all agents)
# ---------------------------------------------------------------------------


def test_inbox_agents_update(mock_http):
    """Test replacing all agents in an inbox."""
    mock_http.patch.return_value = AGENT_PAYLOAD

    resource = InboxMembersResource(mock_http)
    agents = resource.update(account_id=1, inbox_id=5, agent_ids=[10])

    mock_http.patch.assert_called_once_with(
        "/api/v1/accounts/1/inbox_members",
        json={"inbox_id": 5, "user_ids": [10]},
    )
    assert isinstance(agents, list)
    assert len(agents) == 1
    assert isinstance(agents[0], Agent)
    assert agents[0].id == 10


def test_inbox_agents_update_empty_payload(mock_http):
    """Test update returns empty list on empty response."""
    mock_http.patch.return_value = {}

    resource = InboxMembersResource(mock_http)
    agents = resource.update(account_id=1, inbox_id=5, agent_ids=[10])

    assert agents == []


@pytest.mark.asyncio
async def test_async_inbox_agents_update(mock_async_http):
    """Test async replacing all agents in an inbox."""
    mock_async_http.patch = AsyncMock(return_value=AGENT_PAYLOAD)

    resource = AsyncInboxMembersResource(mock_async_http)
    agents = await resource.update(account_id=1, inbox_id=5, agent_ids=[10])

    mock_async_http.patch.assert_called_once_with(
        "/api/v1/accounts/1/inbox_members",
        json={"inbox_id": 5, "user_ids": [10]},
    )
    assert len(agents) == 1
    assert agents[0].name == "Alice"


# ---------------------------------------------------------------------------
# remove (DELETE)
# ---------------------------------------------------------------------------


def test_inbox_agents_remove(mock_http):
    """Test removing agents from an inbox."""
    mock_http.delete.return_value = {}

    resource = InboxMembersResource(mock_http)
    result = resource.remove(account_id=1, inbox_id=5, agent_ids=[10])

    mock_http.delete.assert_called_once_with(
        "/api/v1/accounts/1/inbox_members",
        json={"inbox_id": 5, "user_ids": [10]},
    )
    assert result is None


@pytest.mark.asyncio
async def test_async_inbox_agents_remove(mock_async_http):
    """Test async removing agents from an inbox."""
    mock_async_http.delete = AsyncMock(return_value={})

    resource = AsyncInboxMembersResource(mock_async_http)
    await resource.remove(account_id=1, inbox_id=5, agent_ids=[10])

    mock_async_http.delete.assert_called_once_with(
        "/api/v1/accounts/1/inbox_members",
        json={"inbox_id": 5, "user_ids": [10]},
    )
