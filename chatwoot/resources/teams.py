"""Teams resource for managing teams and team agents."""

from __future__ import annotations

from typing import Any

from chatwoot.resources._base import AsyncBaseResource, BaseResource
from chatwoot.types.agent import Agent
from chatwoot.types.team import Team


class TeamAgentsResource(BaseResource):
    """Nested resource for managing team agents."""

    def list(self, account_id: int, team_id: int) -> list[Agent]:
        """List agents in the team.

        Args:
            account_id: The account ID
            team_id: The team ID

        Returns:
            List of Agent objects in the team

        Examples:
            >>> agents = client.teams.agents.list(account_id=1, team_id=5)
        """
        response = self._http.get(
            f"/api/v1/accounts/{account_id}/teams/{team_id}/team_members"
        )
        if isinstance(response, list):
            return [Agent(**item) for item in response]
        return []

    def add(self, account_id: int, team_id: int, agent_ids: list[int]) -> None:
        """Add agents to the team.

        Args:
            account_id: The account ID
            team_id: The team ID
            agent_ids: List of agent IDs to add

        Examples:
            >>> client.teams.agents.add(
            ...     account_id=1,
            ...     team_id=5,
            ...     agent_ids=[10, 11, 12]
            ...
        """
        data = {"user_ids": agent_ids}
        self._http.post(
            f"/api/v1/accounts/{account_id}/teams/{team_id}/team_members",
            json=data,
        )

    def update(
        self, account_id: int, team_id: int, agent_ids: list[int]
    ) -> list[Agent]:
        """Replace all agents in the team.

        All existing agents will be removed and replaced with the given list.

        Args:
            account_id: The account ID
            team_id: The team ID
            agent_ids: List of agent IDs that will form the new team

        Returns:
            List of Agent objects now in the team

        Examples:
            >>> agents = client.teams.agents.update(
            ...     account_id=1,
            ...     team_id=5,
            ...     agent_ids=[10, 11]
            ... )
        """
        data = {"user_ids": agent_ids}
        response = self._http.patch(
            f"/api/v1/accounts/{account_id}/teams/{team_id}/team_members",
            json=data,
        )
        if isinstance(response, list):
            return [Agent(**item) for item in response]
        return []

    def remove(self, account_id: int, team_id: int, agent_ids: list[int]) -> None:
        """Remove agents from the team.

        Args:
            account_id: The account ID
            team_id: The team ID
            agent_ids: List of agent IDs to remove

        Examples:
            >>> client.teams.agents.remove(
            ...     account_id=1,
            ...     team_id=5,
            ...     agent_ids=[10]
            ...
        """
        data = {"user_ids": agent_ids}
        self._http.delete(
            f"/api/v1/accounts/{account_id}/teams/{team_id}/team_members",
            json=data,
        )


class AsyncTeamAgentsResource(AsyncBaseResource):
    """Async nested resource for managing team agents."""

    async def list(self, account_id: int, team_id: int) -> list[Agent]:
        """List agents in the team (async).

        Args:
            account_id: The account ID
            team_id: The team ID

        Returns:
            List of Agent objects in the team
        """
        response = await self._http.get(
            f"/api/v1/accounts/{account_id}/teams/{team_id}/team_members"
        )
        if isinstance(response, list):
            return [Agent(**item) for item in response]
        return []

    async def add(self, account_id: int, team_id: int, agent_ids: list[int]) -> None:
        """Add agents to the team (async).

        Args:
            account_id: The account ID
            team_id: The team ID
            agent_ids: List of agent IDs to add
        """
        data = {"user_ids": agent_ids}
        await self._http.post(
            f"/api/v1/accounts/{account_id}/teams/{team_id}/team_members",
            json=data,
        )

    async def update(
        self, account_id: int, team_id: int, agent_ids: list[int]
    ) -> list[Agent]:
        """Replace all agents in the team (async).

        All existing agents will be removed and replaced with the given list.

        Args:
            account_id: The account ID
            team_id: The team ID
            agent_ids: List of agent IDs that will form the new team

        Returns:
            List of Agent objects now in the team
        """
        data = {"user_ids": agent_ids}
        response = await self._http.patch(
            f"/api/v1/accounts/{account_id}/teams/{team_id}/team_members",
            json=data,
        )
        if isinstance(response, list):
            return [Agent(**item) for item in response]
        return []

    async def remove(self, account_id: int, team_id: int, agent_ids: list[int]) -> None:
        """Remove agents from the team (async).

        Args:
            account_id: The account ID
            team_id: The team ID
            agent_ids: List of agent IDs to remove
        """
        data = {"user_ids": agent_ids}
        await self._http.delete(
            f"/api/v1/accounts/{account_id}/teams/{team_id}/team_members",
            json=data,
        )


class TeamsResource(BaseResource):
    """Synchronous teams resource."""

    def __init__(self, http):
        """Initialize teams resource with nested agents resource."""
        super().__init__(http)
        self.agents = TeamAgentsResource(http)

    def list(self, account_id: int) -> list[Team]:
        """List all teams in the account.

        Args:
            account_id: The account ID

        Returns:
            List of Team objects

        Examples:
            >>> teams = client.teams.list(account_id=1)
            ... for team in teams:
            ...     print(team.name)
        """
        response = self._http.get(f"/api/v1/accounts/{account_id}/teams")
        if isinstance(response, list):
            return [Team(**item) for item in response]
        return []

    def get(self, account_id: int, team_id: int) -> Team:
        """Get team details.

        Args:
            account_id: The account ID
            team_id: The team ID

        Returns:
            Team object

        Examples:
            >>> team = client.teams.get(account_id=1, team_id=5)
            ... print(team.description)
        """
        response = self._http.get(f"/api/v1/accounts/{account_id}/teams/{team_id}")
        return Team(**response)

    def create(
        self,
        account_id: int,
        name: str,
        **kwargs: Any,
    ) -> Team:
        """Create a new team.

        Args:
            account_id: The account ID
            name: Team name
            **kwargs: Additional team attributes (description, allow_auto_assign)

        Returns:
            Created Team object

        Examples:
            >>> team = client.teams.create(
            ...     account_id=1,
            ...     name="Support Team",
            ...     description="Customer support team",
            ...     allow_auto_assign=True
            ...
        """
        data = {"name": name, **kwargs}
        response = self._http.post(f"/api/v1/accounts/{account_id}/teams", json=data)
        return Team(**response)

    def update(
        self,
        account_id: int,
        team_id: int,
        **kwargs: Any,
    ) -> Team:
        """Update team.

        Args:
            account_id: The account ID
            team_id: The team ID
            **kwargs: Team attributes to update

        Returns:
            Updated Team object

        Examples:
            >>> team = client.teams.update(
            ...     account_id=1,
            ...     team_id=5,
            ...     name="New Team Name"
            ...
        """
        response = self._http.patch(
            f"/api/v1/accounts/{account_id}/teams/{team_id}",
            json=kwargs,
        )
        return Team(**response)

    def delete(self, account_id: int, team_id: int) -> None:
        """Delete team.

        Args:
            account_id: The account ID
            team_id: The team ID

        Examples:
            >>> client.teams.delete(account_id=1, team_id=5)
        """
        self._http.delete(f"/api/v1/accounts/{account_id}/teams/{team_id}")


class AsyncTeamsResource(AsyncBaseResource):
    """Asynchronous teams resource."""

    def __init__(self, http):
        """Initialize async teams resource with nested agents resource."""
        super().__init__(http)
        self.agents = AsyncTeamAgentsResource(http)

    async def list(self, account_id: int) -> list[Team]:
        """List all teams in the account (async).

        Args:
            account_id: The account ID

        Returns:
            List of Team objects
        """
        response = await self._http.get(f"/api/v1/accounts/{account_id}/teams")
        if isinstance(response, list):
            return [Team(**item) for item in response]
        return []

    async def get(self, account_id: int, team_id: int) -> Team:
        """Get team details (async).

        Args:
            account_id: The account ID
            team_id: The team ID

        Returns:
            Team object
        """
        response = await self._http.get(
            f"/api/v1/accounts/{account_id}/teams/{team_id}"
        )
        return Team(**response)

    async def create(
        self,
        account_id: int,
        name: str,
        **kwargs: Any,
    ) -> Team:
        """Create a new team (async).

        Args:
            account_id: The account ID
            name: Team name
            **kwargs: Additional team attributes

        Returns:
            Created Team object
        """
        data = {"name": name, **kwargs}
        response = await self._http.post(
            f"/api/v1/accounts/{account_id}/teams", json=data
        )
        return Team(**response)

    async def update(
        self,
        account_id: int,
        team_id: int,
        **kwargs: Any,
    ) -> Team:
        """Update team (async).

        Args:
            account_id: The account ID
            team_id: The team ID
            **kwargs: Team attributes to update

        Returns:
            Updated Team object
        """
        response = await self._http.patch(
            f"/api/v1/accounts/{account_id}/teams/{team_id}",
            json=kwargs,
        )
        return Team(**response)

    async def delete(self, account_id: int, team_id: int) -> None:
        """Delete team (async).

        Args:
            account_id: The account ID
            team_id: The team ID
        """
        await self._http.delete(f"/api/v1/accounts/{account_id}/teams/{team_id}")
