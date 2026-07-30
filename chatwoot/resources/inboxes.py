"""Inboxes resource for managing inboxes."""

from __future__ import annotations

from typing import Any

from chatwoot.resources._base import AsyncBaseResource, BaseResource
from chatwoot.types.agent import Agent
from chatwoot.types.inbox import Inbox


class InboxMembersResource(BaseResource):
    """Nested resource for managing inbox agents."""

    def list(self, account_id: int, inbox_id: int) -> list[Agent]:
        """List agents in an inbox.

        Args:
            account_id: The account ID
            inbox_id: The inbox ID

        Returns:
            List of Agent objects

        Examples:
            >>> agents = client.inboxes.agents.list(account_id=1, inbox_id=5)
            ... for agent in agents:
            ...     print(agent.name, agent.email)
        """
        response = self._http.get(
            f"/api/v1/accounts/{account_id}/inbox_members/{inbox_id}"
        )
        if isinstance(response, list):
            return [Agent(**item) for item in response]
        return []

    def add(self, account_id: int, inbox_id: int, agent_ids: list[int]) -> list[Agent]:
        """Add agents to an inbox.

        Args:
            account_id: The account ID
            inbox_id: The inbox ID
            agent_ids: List of agent IDs to add

        Returns:
            List of Agent objects in the inbox

        Examples:
            >>> agents = client.inboxes.agents.add(
            ...     account_id=1,
            ...     inbox_id=5,
            ...     agent_ids=[10, 11, 12]
            ... )
        """
        data = {"inbox_id": inbox_id, "user_ids": agent_ids}
        response = self._http.post(
            f"/api/v1/accounts/{account_id}/inbox_members",
            json=data,
        )
        if isinstance(response, list):
            return [Agent(**item) for item in response]
        return []

    def update(
        self, account_id: int, inbox_id: int, agent_ids: list[int]
    ) -> list[Agent]:
        """Replace all agents in an inbox (removes agents not in the list).

        Args:
            account_id: The account ID
            inbox_id: The inbox ID
            agent_ids: List of agent IDs — replaces the current set entirely

        Returns:
            List of Agent objects now in the inbox

        Examples:
            >>> agents = client.inboxes.agents.update(
            ...     account_id=1,
            ...     inbox_id=5,
            ...     agent_ids=[10, 11]
            ... )
        """
        data = {"inbox_id": inbox_id, "user_ids": agent_ids}
        response = self._http.patch(
            f"/api/v1/accounts/{account_id}/inbox_members",
            json=data,
        )
        if isinstance(response, list):
            return [Agent(**item) for item in response]
        return []

    def remove(self, account_id: int, inbox_id: int, agent_ids: list[int]) -> None:
        """Remove agents from an inbox.

        Args:
            account_id: The account ID
            inbox_id: The inbox ID
            agent_ids: List of agent IDs to remove

        Examples:
            >>> client.inboxes.agents.remove(
            ...     account_id=1,
            ...     inbox_id=5,
            ...     agent_ids=[10]
            ... )
        """
        data = {"inbox_id": inbox_id, "user_ids": agent_ids}
        self._http.delete(
            f"/api/v1/accounts/{account_id}/inbox_members",
            json=data,
        )


class AsyncInboxMembersResource(AsyncBaseResource):
    """Async nested resource for managing inbox agents."""

    async def list(self, account_id: int, inbox_id: int) -> list[Agent]:
        """List agents in an inbox (async).

        Args:
            account_id: The account ID
            inbox_id: The inbox ID

        Returns:
            List of Agent objects
        """
        response = await self._http.get(
            f"/api/v1/accounts/{account_id}/inbox_members/{inbox_id}"
        )
        if isinstance(response, list):
            return [Agent(**item) for item in response]
        return []

    async def add(
        self, account_id: int, inbox_id: int, agent_ids: list[int]
    ) -> list[Agent]:
        """Add agents to an inbox (async).

        Args:
            account_id: The account ID
            inbox_id: The inbox ID
            agent_ids: List of agent IDs to add

        Returns:
            List of Agent objects in the inbox
        """
        data = {"inbox_id": inbox_id, "user_ids": agent_ids}
        response = await self._http.post(
            f"/api/v1/accounts/{account_id}/inbox_members",
            json=data,
        )
        if isinstance(response, list):
            return [Agent(**item) for item in response]
        return []

    async def update(
        self, account_id: int, inbox_id: int, agent_ids: list[int]
    ) -> list[Agent]:
        """Replace all agents in an inbox (async).

        Args:
            account_id: The account ID
            inbox_id: The inbox ID
            agent_ids: List of agent IDs — replaces the current set entirely

        Returns:
            List of Agent objects now in the inbox
        """
        data = {"inbox_id": inbox_id, "user_ids": agent_ids}
        response = await self._http.patch(
            f"/api/v1/accounts/{account_id}/inbox_members",
            json=data,
        )
        if isinstance(response, list):
            return [Agent(**item) for item in response]
        return []

    async def remove(
        self, account_id: int, inbox_id: int, agent_ids: list[int]
    ) -> None:
        """Remove agents from an inbox (async).

        Args:
            account_id: The account ID
            inbox_id: The inbox ID
            agent_ids: List of agent IDs to remove
        """
        data = {"inbox_id": inbox_id, "user_ids": agent_ids}
        await self._http.delete(
            f"/api/v1/accounts/{account_id}/inbox_members",
            json=data,
        )


class InboxesResource(BaseResource):
    """Synchronous inboxes resource."""

    def __init__(self, http):
        """Initialize inboxes resource with nested agents resource."""
        super().__init__(http)
        self.agents = InboxMembersResource(http)

    def list(self, account_id: int) -> list[Inbox]:
        """List all inboxes in the account.

        Args:
            account_id: The account ID

        Returns:
            List of Inbox objects

        Raises:
            ChatwootAuthError: If authentication fails
            ChatwootPermissionError: If user doesn't have access

        Examples:
            >>> inboxes = client.inboxes.list(account_id=1)
            >>> for inbox in inboxes:
            ...     print(inbox.name)
        """
        response = self._http.get(f"/api/v1/accounts/{account_id}/inboxes")
        if isinstance(response, list):
            return [Inbox(**item) for item in response]
        return []

    def get(self, account_id: int, inbox_id: int) -> Inbox:
        """Get inbox details.

        Args:
            account_id: The account ID
            inbox_id: The inbox ID

        Returns:
            Inbox object

        Raises:
            ChatwootNotFoundError: If inbox not found
            ChatwootAuthError: If authentication fails

        Examples:
            >>> inbox = client.inboxes.get(account_id=1, inbox_id=5)
            >>> print(inbox.name)
        """
        response = self._http.get(f"/api/v1/accounts/{account_id}/inboxes/{inbox_id}")
        return Inbox(**response)

    def create(
        self,
        account_id: int,
        name: str,
        channel_type: str,
        **kwargs: Any,
    ) -> Inbox:
        """Create a new inbox.

        Args:
            account_id: The account ID
            name: Inbox name
            channel_type: Type of channel (e.g., 'api', 'web_widget')
            **kwargs: Additional inbox attributes

        Returns:
            Created Inbox object

        Raises:
            ChatwootValidationError: If validation fails
            ChatwootAuthError: If authentication fails

        Examples:
            >>> inbox = client.inboxes.create(
            ...     account_id=1,
            ...     name="Support Inbox",
            ...     channel_type="api"
            ... )
        """
        data = {"name": name, "channel": {"type": channel_type, **kwargs}}
        response = self._http.post(f"/api/v1/accounts/{account_id}/inboxes", json=data)
        return Inbox(**response)

    def update(
        self,
        account_id: int,
        inbox_id: int,
        **kwargs: Any,
    ) -> Inbox:
        """Update inbox.

        Args:
            account_id: The account ID
            inbox_id: The inbox ID
            **kwargs: Inbox attributes to update

        Returns:
            Updated Inbox object

        Raises:
            ChatwootNotFoundError: If inbox not found
            ChatwootValidationError: If validation fails

        Examples:
            >>> inbox = client.inboxes.update(
            ...     account_id=1,
            ...     inbox_id=5,
            ...     name="New Name",
            ...     enable_auto_assignment=True
            ... )
        """
        response = self._http.patch(
            f"/api/v1/accounts/{account_id}/inboxes/{inbox_id}",
            json=kwargs,
        )
        return Inbox(**response)

    def get_agent_bot(self, account_id: int, inbox_id: int) -> dict | None:
        """Get the agent bot assigned to an inbox.

        Args:
            account_id: The account ID
            inbox_id: The inbox ID

        Returns:
            Agent bot dict, or None if no bot is assigned

        Examples:
            >>> bot = client.inboxes.get_agent_bot(account_id=1, inbox_id=5)
            >>> if bot:
            ...     print(bot["id"], bot["name"])
        """
        response = self._http.get(
            f"/api/v1/accounts/{account_id}/inboxes/{inbox_id}/agent_bot"
        )
        return response if isinstance(response, dict) else None

    def set_agent_bot(
        self, account_id: int, inbox_id: int, agent_bot_id: int | None
    ) -> None:
        """Assign or remove an agent bot from an inbox.

        Args:
            account_id: The account ID
            inbox_id: The inbox ID
            agent_bot_id: Bot ID to assign, or None to remove the bot

        Examples:
            >>> client.inboxes.set_agent_bot(account_id=1, inbox_id=5, agent_bot_id=2)
            >>> # Remove bot:
            >>> client.inboxes.set_agent_bot(account_id=1, inbox_id=5, agent_bot_id=None)
        """
        self._http.post(
            f"/api/v1/accounts/{account_id}/inboxes/{inbox_id}/set_agent_bot",
            json={"agent_bot": agent_bot_id},
        )


class AsyncInboxesResource(AsyncBaseResource):
    """Asynchronous inboxes resource."""

    def __init__(self, http):
        """Initialize async inboxes resource with nested agents resource."""
        super().__init__(http)
        self.agents = AsyncInboxMembersResource(http)

    async def list(self, account_id: int) -> list[Inbox]:
        """List all inboxes in the account (async).

        Args:
            account_id: The account ID

        Returns:
            List of Inbox objects
        """
        response = await self._http.get(f"/api/v1/accounts/{account_id}/inboxes")
        if isinstance(response, list):
            return [Inbox(**item) for item in response]
        return []

    async def get(self, account_id: int, inbox_id: int) -> Inbox:
        """Get inbox details (async).

        Args:
            account_id: The account ID
            inbox_id: The inbox ID

        Returns:
            Inbox object
        """
        response = await self._http.get(
            f"/api/v1/accounts/{account_id}/inboxes/{inbox_id}"
        )
        return Inbox(**response)

    async def create(
        self,
        account_id: int,
        name: str,
        channel_type: str,
        **kwargs: Any,
    ) -> Inbox:
        """Create a new inbox (async).

        Args:
            account_id: The account ID
            name: Inbox name
            channel_type: Type of channel
            **kwargs: Additional inbox attributes

        Returns:
            Created Inbox object
        """
        data = {"name": name, "channel": {"type": channel_type, **kwargs}}
        response = await self._http.post(
            f"/api/v1/accounts/{account_id}/inboxes", json=data
        )
        return Inbox(**response)

    async def update(
        self,
        account_id: int,
        inbox_id: int,
        **kwargs: Any,
    ) -> Inbox:
        """Update inbox (async).

        Args:
            account_id: The account ID
            inbox_id: The inbox ID
            **kwargs: Inbox attributes to update

        Returns:
            Updated Inbox object
        """
        response = await self._http.patch(
            f"/api/v1/accounts/{account_id}/inboxes/{inbox_id}",
            json=kwargs,
        )
        return Inbox(**response)

    async def get_agent_bot(self, account_id: int, inbox_id: int) -> dict | None:
        """Get the agent bot assigned to an inbox (async).

        Args:
            account_id: The account ID
            inbox_id: The inbox ID

        Returns:
            Agent bot dict, or None if no bot is assigned
        """
        response = await self._http.get(
            f"/api/v1/accounts/{account_id}/inboxes/{inbox_id}/agent_bot"
        )
        return response if isinstance(response, dict) else None

    async def set_agent_bot(
        self, account_id: int, inbox_id: int, agent_bot_id: int | None
    ) -> None:
        """Assign or remove an agent bot from an inbox (async).

        Args:
            account_id: The account ID
            inbox_id: The inbox ID
            agent_bot_id: Bot ID to assign, or None to remove the bot
        """
        await self._http.post(
            f"/api/v1/accounts/{account_id}/inboxes/{inbox_id}/set_agent_bot",
            json={"agent_bot": agent_bot_id},
        )
