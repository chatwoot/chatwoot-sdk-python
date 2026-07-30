"""Tests for inboxes.agents (InboxMembersResource)."""

import pytest
from unittest.mock import AsyncMock

from chatwoot.resources.inboxes import (
    InboxMembersResource,
    AsyncInboxMembersResource,
    InboxesResource,
    AsyncInboxesResource,
)
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
    {
        "id": 11,
        "name": "Bob",
        "email": "bob@example.com",
        "role": "administrator",
        "availability_status": "busy",
        "confirmed": True,
        "account_id": 1,
    },
]


# ---------------------------------------------------------------------------
# list
# ---------------------------------------------------------------------------


def test_inbox_agents_list(mock_http):
    """Test listing agents in an inbox."""
    mock_http.get.return_value = AGENT_PAYLOAD

    resource = InboxMembersResource(mock_http)
    agents = resource.list(account_id=1, inbox_id=5)

    mock_http.get.assert_called_once_with("/api/v1/accounts/1/inbox_members/5")
    assert isinstance(agents, list)
    assert len(agents) == 2
    assert isinstance(agents[0], Agent)
    assert agents[0].id == 10
    assert agents[0].name == "Alice"
    assert agents[1].id == 11
    assert agents[1].role == "administrator"


def test_inbox_agents_list_empty_payload(mock_http):
    """Test listing agents returns empty list when payload is missing."""
    mock_http.get.return_value = {}

    resource = InboxMembersResource(mock_http)
    agents = resource.list(account_id=1, inbox_id=5)

    assert agents == []


# ---------------------------------------------------------------------------
# add
# ---------------------------------------------------------------------------


def test_inbox_agents_add(mock_http):
    """Test adding agents to an inbox."""
    mock_http.post.return_value = AGENT_PAYLOAD

    resource = InboxMembersResource(mock_http)
    agents = resource.add(account_id=1, inbox_id=5, agent_ids=[10, 11])

    mock_http.post.assert_called_once_with(
        "/api/v1/accounts/1/inbox_members",
        json={"inbox_id": 5, "user_ids": [10, 11]},
    )
    assert isinstance(agents, list)
    assert len(agents) == 2
    assert isinstance(agents[0], Agent)
    assert agents[0].id == 10


def test_inbox_agents_add_empty_response(mock_http):
    """Test adding agents returns empty list on empty response."""
    mock_http.post.return_value = {}

    resource = InboxMembersResource(mock_http)
    agents = resource.add(account_id=1, inbox_id=5, agent_ids=[10])

    assert agents == []


# ---------------------------------------------------------------------------
# nested resource wiring
# ---------------------------------------------------------------------------


def test_inboxes_resource_has_agents(mock_http):
    """Test InboxesResource exposes agents as a nested resource."""
    resource = InboxesResource(mock_http)
    assert hasattr(resource, "agents")
    assert isinstance(resource.agents, InboxMembersResource)


def test_async_inboxes_resource_has_agents(mock_async_http):
    """Test AsyncInboxesResource exposes agents as a nested resource."""
    resource = AsyncInboxesResource(mock_async_http)
    assert hasattr(resource, "agents")
    assert isinstance(resource.agents, AsyncInboxMembersResource)


# ---------------------------------------------------------------------------
# async variants
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_async_inbox_agents_list(mock_async_http):
    """Test async listing agents in an inbox."""
    mock_async_http.get = AsyncMock(return_value=AGENT_PAYLOAD)

    resource = AsyncInboxMembersResource(mock_async_http)
    agents = await resource.list(account_id=1, inbox_id=5)

    mock_async_http.get.assert_called_once_with("/api/v1/accounts/1/inbox_members/5")
    assert isinstance(agents, list)
    assert len(agents) == 2
    assert agents[0].name == "Alice"


@pytest.mark.asyncio
async def test_async_inbox_agents_add(mock_async_http):
    """Test async adding agents to an inbox."""
    mock_async_http.post = AsyncMock(return_value=AGENT_PAYLOAD)

    resource = AsyncInboxMembersResource(mock_async_http)
    agents = await resource.add(account_id=1, inbox_id=5, agent_ids=[10, 11])

    mock_async_http.post.assert_called_once_with(
        "/api/v1/accounts/1/inbox_members",
        json={"inbox_id": 5, "user_ids": [10, 11]},
    )
    assert len(agents) == 2
    assert agents[1].id == 11
