"""Smoke tests that hit a real local Chatwoot instance.

Run with:
    uv run pytest tests/smoke/ -v --url=http://localhost:3000 --account-id=1 --token=YOUR_TOKEN

Tests are ordered to build on each other: earlier tests populate ``state``
with resource IDs that later tests consume.
"""

from __future__ import annotations

import uuid

import pytest

from chatwoot import ChatwootClient
from chatwoot.types.agent import Agent
from chatwoot.types.contact import Contact, ContactCreateResponse
from chatwoot.types.conversation import Conversation, ConversationToggleStatusResponse
from chatwoot.types.inbox import Inbox
from chatwoot.types.message import Message
from chatwoot.types.profile import Profile
from chatwoot.types.team import Team

PREFIX = "sdk-smoke-"


def _uid() -> str:
    return uuid.uuid4().hex[:8]


# ---------------------------------------------------------------------------
# Helpers for cleanup
# ---------------------------------------------------------------------------


def _cleanup(client: ChatwootClient, account_id: int, state: dict) -> None:
    """Best-effort cleanup of resources created during the run."""
    cid = state.get("contact_id")
    if cid:
        try:
            client.contacts.delete(account_id, cid)
        except Exception:
            pass

    tid = state.get("team_id")
    if tid:
        try:
            client.teams.delete(account_id, tid)
        except Exception:
            pass


@pytest.fixture(scope="module", autouse=True)
def _teardown(client: ChatwootClient, account_id: int, state: dict):
    """Run all tests, then clean up."""
    yield
    _cleanup(client, account_id, state)


# ---------------------------------------------------------------------------
# 1. Profile
# ---------------------------------------------------------------------------


class TestProfile:
    def test_get_profile(self, client: ChatwootClient, state: dict):
        profile = client.profile.get()
        assert isinstance(profile, Profile)
        assert profile.id > 0
        assert profile.name
        state["agent_id"] = profile.id


# ---------------------------------------------------------------------------
# 2. Agents
# ---------------------------------------------------------------------------


class TestAgents:
    def test_list_agents(self, client: ChatwootClient, account_id: int, state: dict):
        agents = client.agents.list(account_id)
        assert isinstance(agents, list)
        assert len(agents) >= 1
        assert isinstance(agents[0], Agent)
        assert agents[0].id > 0
        # Keep first agent id for later use
        state["agent_id"] = agents[0].id


# ---------------------------------------------------------------------------
# 3. Inboxes
# ---------------------------------------------------------------------------


class TestInboxes:
    def test_list_or_create_inbox(
        self, client: ChatwootClient, account_id: int, state: dict
    ):
        inboxes = client.inboxes.list(account_id)
        assert isinstance(inboxes, list)

        # Prefer an existing API-type inbox; fall back to creating one
        api_inbox = next(
            (i for i in inboxes if "api" in (i.channel_type or "").lower()), None
        )
        if api_inbox:
            state["inbox_id"] = api_inbox.id
        elif inboxes:
            state["inbox_id"] = inboxes[0].id
        else:
            inbox = client.inboxes.create(
                account_id,
                name=f"{PREFIX}inbox-{_uid()}",
                channel_type="api",
            )
            assert isinstance(inbox, Inbox)
            assert inbox.id > 0
            state["inbox_id"] = inbox.id

    def test_get_inbox(self, client: ChatwootClient, account_id: int, state: dict):
        inbox = client.inboxes.get(account_id, state["inbox_id"])
        assert isinstance(inbox, Inbox)
        assert inbox.id == state["inbox_id"]

    def test_inbox_agents_list(
        self, client: ChatwootClient, account_id: int, state: dict
    ):
        agents = client.inboxes.agents.list(account_id, state["inbox_id"])
        assert isinstance(agents, list)
        for agent in agents:
            assert isinstance(agent, Agent)

    def test_inbox_agents_add(
        self, client: ChatwootClient, account_id: int, state: dict
    ):
        agents = client.inboxes.agents.add(
            account_id, state["inbox_id"], agent_ids=[state["agent_id"]]
        )
        assert isinstance(agents, list)
        assert any(a.id == state["agent_id"] for a in agents)


# ---------------------------------------------------------------------------
# 4. Teams  (create -> get -> update -> list -> delete)
# ---------------------------------------------------------------------------


class TestTeams:
    def test_create_team(self, client: ChatwootClient, account_id: int, state: dict):
        name = f"{PREFIX}team-{_uid()}"
        team = client.teams.create(account_id, name=name, description="smoke test team")
        assert isinstance(team, Team)
        assert team.id > 0
        assert team.name == name
        state["team_id"] = team.id
        state["team_name"] = name

    def test_get_team(self, client: ChatwootClient, account_id: int, state: dict):
        team = client.teams.get(account_id, state["team_id"])
        assert isinstance(team, Team)
        assert team.id == state["team_id"]

    def test_update_team(self, client: ChatwootClient, account_id: int, state: dict):
        new_name = f"{PREFIX}team-updated-{_uid()}"
        team = client.teams.update(account_id, state["team_id"], name=new_name)
        assert isinstance(team, Team)
        assert team.name == new_name
        state["team_name"] = new_name

    def test_list_teams(self, client: ChatwootClient, account_id: int, state: dict):
        teams = client.teams.list(account_id)
        assert isinstance(teams, list)
        ids = [t.id for t in teams]
        assert state["team_id"] in ids


# ---------------------------------------------------------------------------
# 5. Team Agents
# ---------------------------------------------------------------------------


class TestTeamAgents:
    def test_add_agent_to_team(
        self, client: ChatwootClient, account_id: int, state: dict
    ):
        client.teams.agents.add(
            account_id, state["team_id"], agent_ids=[state["agent_id"]]
        )

    def test_list_team_agents(
        self, client: ChatwootClient, account_id: int, state: dict
    ):
        agents = client.teams.agents.list(account_id, state["team_id"])
        assert isinstance(agents, list)
        assert any(a.id == state["agent_id"] for a in agents)

    def test_remove_agent_from_team(
        self, client: ChatwootClient, account_id: int, state: dict
    ):
        client.teams.agents.remove(
            account_id, state["team_id"], agent_ids=[state["agent_id"]]
        )
        agents = client.teams.agents.list(account_id, state["team_id"])
        assert not any(a.id == state["agent_id"] for a in agents)


# ---------------------------------------------------------------------------
# 6. Contacts
# ---------------------------------------------------------------------------


class TestContacts:
    def test_create_contact(self, client: ChatwootClient, account_id: int, state: dict):
        uid = _uid()
        result = client.contacts.create(
            account_id,
            inbox_id=state["inbox_id"],
            name=f"{PREFIX}contact-{uid}",
            email=f"{PREFIX}{uid}@example.com",
        )
        assert isinstance(result, ContactCreateResponse)
        assert isinstance(result.contact, Contact)
        assert result.contact.id > 0
        assert result.contact_inbox.source_id
        state["contact_id"] = result.contact.id
        state["contact_email"] = f"{PREFIX}{uid}@example.com"
        state["source_id"] = result.contact_inbox.source_id

    def test_get_contact(self, client: ChatwootClient, account_id: int, state: dict):
        contact = client.contacts.get(account_id, state["contact_id"])
        assert isinstance(contact, Contact)
        assert contact.id == state["contact_id"]

    def test_update_contact(self, client: ChatwootClient, account_id: int, state: dict):
        contact = client.contacts.update(
            account_id, state["contact_id"], name=f"{PREFIX}contact-updated"
        )
        assert isinstance(contact, Contact)
        assert "updated" in contact.name

    def test_search_contact(self, client: ChatwootClient, account_id: int, state: dict):
        contacts = client.contacts.search(account_id, query=state["contact_email"])
        assert isinstance(contacts, list)
        assert any(c.id == state["contact_id"] for c in contacts)

    def test_list_contacts(self, client: ChatwootClient, account_id: int, state: dict):
        contacts = client.contacts.list(account_id)
        assert isinstance(contacts, list)
        assert len(contacts) >= 1

    def test_contact_labels(self, client: ChatwootClient, account_id: int, state: dict):
        labels = client.contacts.labels.add(
            account_id, state["contact_id"], labels=["sdk-smoke-label"]
        )
        assert isinstance(labels, list)
        assert "sdk-smoke-label" in labels

        labels = client.contacts.labels.list(account_id, state["contact_id"])
        assert isinstance(labels, list)
        assert "sdk-smoke-label" in labels

    def test_contact_conversations(
        self, client: ChatwootClient, account_id: int, state: dict
    ):
        convos = client.contacts.conversations(account_id, state["contact_id"])
        assert isinstance(convos, list)

    def test_contactable_inboxes(
        self, client: ChatwootClient, account_id: int, state: dict
    ):
        inboxes = client.contacts.contactable_inboxes(account_id, state["contact_id"])
        assert isinstance(inboxes, list)
        # Each item should have source_id and inbox keys
        for item in inboxes:
            assert "source_id" in item
            assert "inbox" in item
            assert "id" in item["inbox"]


# ---------------------------------------------------------------------------
# 7. Conversations
# ---------------------------------------------------------------------------


class TestConversations:
    def test_create_conversation(
        self, client: ChatwootClient, account_id: int, state: dict
    ):
        source_id = state.get("source_id", f"{PREFIX}src-{_uid()}")
        conversation = client.conversations.create(
            account_id,
            source_id=source_id,
            inbox_id=state["inbox_id"],
            contact_id=state["contact_id"],
        )
        assert isinstance(conversation, Conversation)
        assert conversation.id > 0
        state["conversation_id"] = conversation.id

    def test_get_conversation(
        self, client: ChatwootClient, account_id: int, state: dict
    ):
        convo = client.conversations.get(account_id, state["conversation_id"])
        assert isinstance(convo, Conversation)
        assert convo.id == state["conversation_id"]

    def test_update_conversation(
        self, client: ChatwootClient, account_id: int, state: dict
    ):
        convo = client.conversations.update(
            account_id, state["conversation_id"], priority="high"
        )
        assert isinstance(convo, Conversation)
        assert convo.priority == "high"

    def test_assign_conversation(
        self, client: ChatwootClient, account_id: int, state: dict
    ):
        agent = client.conversations.assign(
            account_id, state["conversation_id"], assignee_id=state["agent_id"]
        )
        assert isinstance(agent, Agent)
        assert agent.id == state["agent_id"]

    def test_list_conversations(
        self, client: ChatwootClient, account_id: int, state: dict
    ):
        convos = client.conversations.list(account_id)
        assert isinstance(convos, list)

    def test_toggle_status(self, client: ChatwootClient, account_id: int, state: dict):
        result = client.conversations.toggle_status(
            account_id, state["conversation_id"], status="resolved"
        )
        assert isinstance(result, ConversationToggleStatusResponse)
        assert result.success is True
        assert result.current_status == "resolved"

    def test_get_counts(self, client: ChatwootClient, account_id: int, state: dict):
        counts = client.conversations.get_counts(account_id)
        assert isinstance(counts, dict)

    def test_conversation_labels(
        self, client: ChatwootClient, account_id: int, state: dict
    ):
        labels = client.conversations.labels.add(
            account_id, state["conversation_id"], labels=["sdk-smoke-label"]
        )
        assert isinstance(labels, list)
        assert "sdk-smoke-label" in labels

        labels = client.conversations.labels.list(account_id, state["conversation_id"])
        assert isinstance(labels, list)
        assert "sdk-smoke-label" in labels


# ---------------------------------------------------------------------------
# 8. Messages
# ---------------------------------------------------------------------------


class TestMessages:
    def test_create_message(self, client: ChatwootClient, account_id: int, state: dict):
        msg = client.messages.create(
            account_id,
            conversation_id=state["conversation_id"],
            content=f"{PREFIX}hello from SDK smoke test",
            message_type="outgoing",
        )
        assert isinstance(msg, Message)
        assert msg.id > 0
        assert PREFIX in (msg.content or "")
        state["message_id"] = msg.id

    def test_list_messages(self, client: ChatwootClient, account_id: int, state: dict):
        messages = client.messages.list(account_id, state["conversation_id"])
        assert isinstance(messages, list)
        assert any(m.id == state["message_id"] for m in messages)


# ---------------------------------------------------------------------------
# 9. Final cleanup: delete team (contact cleaned by _teardown fixture)
# ---------------------------------------------------------------------------


class TestCleanup:
    def test_delete_team(self, client: ChatwootClient, account_id: int, state: dict):
        client.teams.delete(account_id, state["team_id"])
        teams = client.teams.list(account_id)
        assert state["team_id"] not in [t.id for t in teams]
        # Mark as cleaned so _teardown doesn't try again
        del state["team_id"]
