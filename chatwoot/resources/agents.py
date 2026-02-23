"""Agents resource for managing account agents."""

from __future__ import annotations

from typing import Any

from chatwoot.resources._base import AsyncBaseResource, BaseResource
from chatwoot.types.agent import Agent


class AgentsResource(BaseResource):
    """Synchronous agents resource."""

    def list(self, account_id: int) -> list[Agent]:
        """List all agents in the account.

        Args:
            account_id: The account ID

        Returns:
            List of Agent objects

        Raises:
            ChatwootAuthError: If authentication fails
            ChatwootPermissionError: If user doesn't have access

        Examples:
            >>> agents = client.agents.list(account_id=1)
            ... for agent in agents:
            ...     print(agent.name, agent.role)
        """
        response = self._http.get(f"/api/v1/accounts/{account_id}/agents")
        if isinstance(response, list):
            return [Agent(**item) for item in response]
        return []

    def add(
        self,
        account_id: int,
        name: str,
        email: str,
        role: str,
        **kwargs: Any,
    ) -> Agent:
        """Add a new agent to the account.

        Args:
            account_id: The account ID
            name: Agent's name
            email: Agent's email
            role: Agent's role ('agent' or 'administrator')
            **kwargs: Additional agent attributes

        Returns:
            Created Agent object

        Raises:
            ChatwootValidationError: If validation fails
            ChatwootAuthError: If authentication fails

        Examples:
            >>> agent = client.agents.add(
            ...     account_id=1,
            ...     name=\"John Doe\",
            ...     email=\"john@example.com\",
            ...     role=\"agent\"
            ... )
        """
        data = {"name": name, "email": email, "role": role, **kwargs}
        response = self._http.post(f"/api/v1/accounts/{account_id}/agents", json=data)
        return Agent(**response)

    def update(
        self,
        account_id: int,
        agent_id: int,
        **kwargs: Any,
    ) -> Agent:
        """Update agent details.

        Args:
            account_id: The account ID
            agent_id: The agent ID
            **kwargs: Agent attributes to update

        Returns:
            Updated Agent object

        Raises:
            ChatwootNotFoundError: If agent not found
            ChatwootValidationError: If validation fails

        Examples:
            >>> agent = client.agents.update(
            ...     account_id=1,
            ...     agent_id=10,
            ...     name=\"Jane Doe\",
            ...     role=\"administrator\"
            ... )
        """
        response = self._http.patch(
            f"/api/v1/accounts/{account_id}/agents/{agent_id}",
            json=kwargs,
        )
        return Agent(**response)

    def remove(self, account_id: int, agent_id: int) -> None:
        """Remove agent from the account.

        Args:
            account_id: The account ID
            agent_id: The agent ID to remove

        Raises:
            ChatwootNotFoundError: If agent not found
            ChatwootPermissionError: If user doesn't have permission

        Examples:
            >>> client.agents.remove(account_id=1, agent_id=10)
        """
        self._http.delete(f"/api/v1/accounts/{account_id}/agents/{agent_id}")


class AsyncAgentsResource(AsyncBaseResource):
    """Asynchronous agents resource."""

    async def list(self, account_id: int) -> list[Agent]:
        """List all agents in the account (async).

        Args:
            account_id: The account ID

        Returns:
            List of Agent objects
        """
        response = await self._http.get(f"/api/v1/accounts/{account_id}/agents")
        if isinstance(response, list):
            return [Agent(**item) for item in response]
        return []

    async def add(
        self,
        account_id: int,
        name: str,
        email: str,
        role: str,
        **kwargs: Any,
    ) -> Agent:
        """Add a new agent to the account (async).

        Args:
            account_id: The account ID
            name: Agent's name
            email: Agent's email
            role: Agent's role
            **kwargs: Additional agent attributes

        Returns:
            Created Agent object
        """
        data = {"name": name, "email": email, "role": role, **kwargs}
        response = await self._http.post(
            f"/api/v1/accounts/{account_id}/agents", json=data
        )
        return Agent(**response)

    async def update(
        self,
        account_id: int,
        agent_id: int,
        **kwargs: Any,
    ) -> Agent:
        """Update agent details (async).

        Args:
            account_id: The account ID
            agent_id: The agent ID
            **kwargs: Agent attributes to update

        Returns:
            Updated Agent object
        """
        response = await self._http.patch(
            f"/api/v1/accounts/{account_id}/agents/{agent_id}",
            json=kwargs,
        )
        return Agent(**response)

    async def remove(self, account_id: int, agent_id: int) -> None:
        """Remove agent from the account (async).

        Args:
            account_id: The account ID
            agent_id: The agent ID to remove
        """
        await self._http.delete(f"/api/v1/accounts/{account_id}/agents/{agent_id}")
