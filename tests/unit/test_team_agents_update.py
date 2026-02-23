"""Tests for teams.agents.update (replace team members)."""

import pytest
from unittest.mock import AsyncMock

from chatwoot.resources.teams import TeamAgentsResource, AsyncTeamAgentsResource
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
# sync update
# ---------------------------------------------------------------------------


def test_team_agents_update_calls_patch(mock_http):
    """update() must use PATCH, not POST."""
    mock_http.patch.return_value = AGENT_PAYLOAD

    resource = TeamAgentsResource(mock_http)
    resource.update(account_id=1, team_id=5, agent_ids=[10, 11])

    mock_http.patch.assert_called_once_with(
        "/api/v1/accounts/1/teams/5/team_members",
        json={"user_ids": [10, 11]},
    )
    mock_http.post.assert_not_called()


def test_team_agents_update_returns_agents(mock_http):
    """update() returns the new list of Agent objects."""
    mock_http.patch.return_value = AGENT_PAYLOAD

    resource = TeamAgentsResource(mock_http)
    agents = resource.update(account_id=1, team_id=5, agent_ids=[10, 11])

    assert isinstance(agents, list)
    assert len(agents) == 2
    assert isinstance(agents[0], Agent)
    assert agents[0].id == 10
    assert agents[1].id == 11


def test_team_agents_update_empty_response(mock_http):
    """update() returns empty list when response is not a list."""
    mock_http.patch.return_value = {}

    resource = TeamAgentsResource(mock_http)
    agents = resource.update(account_id=1, team_id=5, agent_ids=[10])

    assert agents == []


# ---------------------------------------------------------------------------
# async update
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_async_team_agents_update_calls_patch(mock_async_http):
    """Async update() must use PATCH, not POST."""
    mock_async_http.patch = AsyncMock(return_value=AGENT_PAYLOAD)

    resource = AsyncTeamAgentsResource(mock_async_http)
    await resource.update(account_id=1, team_id=5, agent_ids=[10, 11])

    mock_async_http.patch.assert_called_once_with(
        "/api/v1/accounts/1/teams/5/team_members",
        json={"user_ids": [10, 11]},
    )
    mock_async_http.post.assert_not_called()


@pytest.mark.asyncio
async def test_async_team_agents_update_returns_agents(mock_async_http):
    """Async update() returns the new list of Agent objects."""
    mock_async_http.patch = AsyncMock(return_value=AGENT_PAYLOAD)

    resource = AsyncTeamAgentsResource(mock_async_http)
    agents = await resource.update(account_id=1, team_id=5, agent_ids=[10, 11])

    assert len(agents) == 2
    assert agents[0].name == "Alice"
    assert agents[1].role == "administrator"
