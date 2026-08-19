"""Conversations resource for managing conversations."""

from __future__ import annotations

from typing import Any

from chatwoot.resources._base import AsyncBaseResource, BaseResource
from chatwoot.types.common import Unset, UNSET
from chatwoot.types.profile import Profile
from chatwoot.types.conversation import Conversation, ConversationToggleStatusResponse


class ConversationLabelsResource(BaseResource):
    """Nested resource for managing conversation labels."""

    def list(self, account_id: int, conversation_id: int) -> list[str]:
        """List conversation labels.

        Args:
            account_id: The account ID
            conversation_id: The conversation ID

        Returns:
            List of label strings

        Examples:
            >>> labels = client.conversations.labels.list(
            ... account_id=1,
            ... conversation_id=42
            ... )
        """
        response = self._http.get(
            f"/api/v1/accounts/{account_id}/conversations/{conversation_id}/labels"
        )
        if isinstance(response, dict) and "payload" in response:
            return response["payload"]
        return response if isinstance(response, list) else []

    def add(
        self, account_id: int, conversation_id: int, labels: list[str]
    ) -> list[str]:
        """Add/replace labels on conversation.

        IMPORTANT: This overwrites existing labels, does not append.

        Args:
            account_id: The account ID
            conversation_id: The conversation ID
            labels: List of label strings to set

        Returns:
            Updated list of labels

        Examples:
            >>> labels = client.conversations.labels.add(
            ... account_id=1,
            ... conversation_id=42,
            ... labels=["urgent", "billing"]
            ... )
        """
        data = {"labels": labels}
        response = self._http.post(
            f"/api/v1/accounts/{account_id}/conversations/{conversation_id}/labels",
            json=data,
        )
        if isinstance(response, dict) and "payload" in response:
            return response["payload"]
        return response if isinstance(response, list) else []


class AsyncConversationLabelsResource(AsyncBaseResource):
    """Async nested resource for managing conversation labels."""

    async def list(self, account_id: int, conversation_id: int) -> list[str]:
        """List conversation labels (async).

        Args:
            account_id: The account ID
            conversation_id: The conversation ID

        Returns:
            List of label strings
        """
        response = await self._http.get(
            f"/api/v1/accounts/{account_id}/conversations/{conversation_id}/labels"
        )
        if isinstance(response, dict) and "payload" in response:
            return response["payload"]
        return response if isinstance(response, list) else []

    async def add(
        self, account_id: int, conversation_id: int, labels: list[str]
    ) -> list[str]:
        """Add/replace labels on conversation (async).

        IMPORTANT: This overwrites existing labels, does not append.

        Args:
            account_id: The account ID
            conversation_id: The conversation ID
            labels: List of label strings to set

        Returns:
            Updated list of labels
        """
        data = {"labels": labels}
        response = await self._http.post(
            f"/api/v1/accounts/{account_id}/conversations/{conversation_id}/labels",
            json=data,
        )
        if isinstance(response, dict) and "payload" in response:
            return response["payload"]
        return response if isinstance(response, list) else []


class ConversationsResource(BaseResource):
    """Synchronous conversations resource."""

    def __init__(self, http):
        """Initialize conversations resource with nested labels resource."""
        super().__init__(http)
        self.labels = ConversationLabelsResource(http)

    def list(
        self,
        account_id: int,
        status: str = "open",
        assignee_type: str = "all",
        page: int = 1,
        inbox_id: int | None = None,
        team_id: int | None = None,
        labels: list[str] | None = None,
        q: str | None = None,
    ) -> list[Conversation]:
        """List conversations with filters.

        Args:
            account_id: The account ID
            status: Conversation status ('open', 'resolved', 'pending', 'snoozed')
            assignee_type: Filter by assignee ('all', 'me', 'unassigned')
            page: Page number for pagination
            inbox_id: Filter by inbox ID (optional)
            team_id: Filter by team ID (optional)
            labels: Filter by labels (optional)
            q: Search query (optional)

        Returns:
            List of Conversation objects

        Examples:
            >>> conversations = client.conversations.list(
            ... account_id=1,
            ... status="open",
            ... assignee_type="me",
            ... page=1
            ... )
        """
        params: dict[str, Any] = {
            "status": status,
            "assignee_type": assignee_type,
            "page": page,
        }

        if inbox_id is not None:
            params["inbox_id"] = inbox_id
        if team_id is not None:
            params["team_id"] = team_id
        if labels:
            params["labels[]"] = labels
        if q:
            params["q"] = q

        response = self._http.get(
            f"/api/v1/accounts/{account_id}/conversations",
            params=params,
        )
        if isinstance(response, list):
            return [Conversation(**item) for item in response]
        return []

    def get(self, account_id: int, conversation_id: int) -> Conversation:
        """Get conversation details.

        Args:
            account_id: The account ID
            conversation_id: The conversation ID

        Returns:
            Conversation object

        Examples:
            >>> conversation = client.conversations.get(account_id=1, conversation_id=42)
        """
        response = self._http.get(
            f"/api/v1/accounts/{account_id}/conversations/{conversation_id}"
        )
        return Conversation(**response)

    def create(
        self,
        account_id: int,
        source_id: str,
        inbox_id: int,
        contact_id: int | None = None,
        **kwargs: Any,
    ) -> Conversation:
        """Create a new conversation.

        Args:
            account_id: The account ID
            source_id: Unique identifier for the conversation source
            inbox_id: The inbox ID
            contact_id: The contact ID (optional)
            **kwargs: Additional conversation attributes

        Returns:
            Created Conversation object

        Examples:
            >>> conversation = client.conversations.create(
            ... account_id=1,
            ... source_id="user-123",
            ... inbox_id=5,
            ... contact_id=100
            ... )
        """
        data = {
            "source_id": source_id,
            "inbox_id": inbox_id,
            **kwargs,
        }
        if contact_id is not None:
            data["contact_id"] = contact_id

        response = self._http.post(
            f"/api/v1/accounts/{account_id}/conversations",
            json=data,
        )
        return Conversation(**response)

    def update(
        self,
        account_id: int,
        conversation_id: int,
        status: str | None = None,
        assignee_id: int | None = None,
        team_id: int | None = None,
        **kwargs: Any,
    ) -> Conversation:
        """Update conversation.

        Args:
            account_id: The account ID
            conversation_id: The conversation ID
            status: New status (optional)
            assignee_id: New assignee ID (optional)
            team_id: New team ID (optional)
            **kwargs: Additional conversation attributes to update

        Returns:
            Updated Conversation object

        Examples:
            >>> conversation = client.conversations.update(
            ... account_id=1,
            ... conversation_id=42,
            ... status="resolved",
            ... assignee_id=10
            ... )
        """
        data = {**kwargs}
        if status is not None:
            data["status"] = status
        if assignee_id is not None:
            data["assignee_id"] = assignee_id
        if team_id is not None:
            data["team_id"] = team_id

        response = self._http.patch(
            f"/api/v1/accounts/{account_id}/conversations/{conversation_id}",
            json=data,
        )
        return Conversation(**response)

    def assign(
        self,
        account_id: int,
        conversation_id: int,
        assignee_id: int | Unset | None = UNSET,
        team_id: int | Unset | None = UNSET,
    ) -> Conversation:
        """Assign conversation to an agent.

        Args:
            account_id: The account ID
            conversation_id: The conversation ID
            assignee_id: Agent ID to assign to
            team_id: Team ID to assign to

        Returns:
            Profile object

        Examples:
            >>> conversation = client.conversations.assign(
            ... account_id=1,
            ... conversation_id=42,
            ... assignee_id=1
            ... )
        """
        data = {}
        if assignee_id is not UNSET:
            data["assignee_id"] = assignee_id
        if team_id is not UNSET:
            data["team_id"] = team_id

        response = self._http.post(
            f"/api/v1/accounts/{account_id}/conversations/{conversation_id}/assignments",
            json=data,
        )
        return Profile(**response)

    def toggle_status(
        self,
        account_id: int,
        conversation_id: int,
        status: str,
    ) -> ConversationToggleStatusResponse:
        """Toggle conversation status.

        Args:
            account_id: The account ID
            conversation_id: The conversation ID
            status: New status ('open', 'resolved', 'pending', 'snoozed')

        Returns:
            ConversationToggleStatusResponse

        Examples:
            >>> result = client.conversations.toggle_status(
            ... account_id=1,
            ... conversation_id=42,
            ... status="resolved"
            ... )
            ... print(result.current_status)
        """
        data = {"status": status}
        response = self._http.post(
            f"/api/v1/accounts/{account_id}/conversations/{conversation_id}/toggle_status",
            json=data,
        )
        return ConversationToggleStatusResponse(**response)

    def get_counts(
        self,
        account_id: int,
        status: str = "open",
        **filters: Any,
    ) -> dict:
        """Get conversation counts.

        Args:
            account_id: The account ID
            status: Status to count ('open', 'resolved', etc.)
            **filters: Additional filters (inbox_id, team_id, labels, etc.)

        Returns:
            Dictionary with conversation counts

        Examples:
            >>> counts = client.conversations.get_counts(account_id=1, status="open")
            ... print(counts)
        """
        params = {"status": status, **filters}
        response = self._http.get(
            f"/api/v1/accounts/{account_id}/conversations/meta",
            params=params,
        )
        return response if isinstance(response, dict) else {}


class AsyncConversationsResource(AsyncBaseResource):
    """Asynchronous conversations resource."""

    def __init__(self, http):
        """Initialize async conversations resource with nested labels resource."""
        super().__init__(http)
        self.labels = AsyncConversationLabelsResource(http)

    async def list(
        self,
        account_id: int,
        status: str = "open",
        assignee_type: str = "all",
        page: int = 1,
        inbox_id: int | None = None,
        team_id: int | None = None,
        labels: list[str] | None = None,
        q: str | None = None,
    ) -> list[Conversation]:
        """List conversations with filters (async).

        Args:
            account_id: The account ID
            status: Conversation status
            assignee_type: Filter by assignee
            page: Page number
            inbox_id: Filter by inbox ID
            team_id: Filter by team ID
            labels: Filter by labels
            q: Search query

        Returns:
            List of Conversation objects
        """
        params: dict[str, Any] = {
            "status": status,
            "assignee_type": assignee_type,
            "page": page,
        }

        if inbox_id is not None:
            params["inbox_id"] = inbox_id
        if team_id is not None:
            params["team_id"] = team_id
        if labels:
            params["labels[]"] = labels
        if q:
            params["q"] = q

        response = await self._http.get(
            f"/api/v1/accounts/{account_id}/conversations",
            params=params,
        )
        if isinstance(response, list):
            return [Conversation(**item) for item in response]
        return []

    async def get(self, account_id: int, conversation_id: int) -> Conversation:
        """Get conversation details (async).

        Args:
            account_id: The account ID
            conversation_id: The conversation ID

        Returns:
            Conversation object
        """
        response = await self._http.get(
            f"/api/v1/accounts/{account_id}/conversations/{conversation_id}"
        )
        return Conversation(**response)

    async def create(
        self,
        account_id: int,
        source_id: str,
        inbox_id: int,
        contact_id: int | None = None,
        **kwargs: Any,
    ) -> Conversation:
        """Create a new conversation (async).

        Args:
            account_id: The account ID
            source_id: Unique identifier for the conversation source
            inbox_id: The inbox ID
            contact_id: The contact ID
            **kwargs: Additional conversation attributes

        Returns:
            Created Conversation object
        """
        data = {
            "source_id": source_id,
            "inbox_id": inbox_id,
            **kwargs,
        }
        if contact_id is not None:
            data["contact_id"] = contact_id

        response = await self._http.post(
            f"/api/v1/accounts/{account_id}/conversations",
            json=data,
        )
        return Conversation(**response)

    async def update(
        self,
        account_id: int,
        conversation_id: int,
        status: str | None = None,
        assignee_id: int | None = None,
        team_id: int | None = None,
        **kwargs: Any,
    ) -> Conversation:
        """Update conversation (async).

        Args:
            account_id: The account ID
            conversation_id: The conversation ID
            status: New status
            assignee_id: New assignee ID
            team_id: New team ID
            **kwargs: Additional conversation attributes

        Returns:
            Updated Conversation object
        """
        data = {**kwargs}
        if status is not None:
            data["status"] = status
        if assignee_id is not None:
            data["assignee_id"] = assignee_id
        if team_id is not None:
            data["team_id"] = team_id

        response = await self._http.patch(
            f"/api/v1/accounts/{account_id}/conversations/{conversation_id}",
            json=data,
        )
        return Conversation(**response)

    async def assign(
        self,
        account_id: int,
        conversation_id: int,
        assignee_id: int | Unset | None = UNSET,
        team_id: int | Unset | None = UNSET,
    ) -> Conversation:
        """Assign conversation to an agent.

        Args:
            account_id: The account ID
            conversation_id: The conversation ID
            assignee_id: Agent ID to assign to
            team_id: Team ID to assign to

        Returns:
            Profile object

        Examples:
            >>> conversation = client.conversations.assign(
            ... account_id=1,
            ... conversation_id=42,
            ... assignee_id=1
            ... )
        """
        data = {}
        if assignee_id is not UNSET:
            data["assignee_id"] = assignee_id
        if team_id is not UNSET:
            data["team_id"] = team_id

        response = await self._http.post(
            f"/api/v1/accounts/{account_id}/conversations/{conversation_id}/assignments",
            json=data,
        )
        return Profile(**response)

    async def toggle_status(
        self,
        account_id: int,
        conversation_id: int,
        status: str,
    ) -> ConversationToggleStatusResponse:
        """Toggle conversation status (async).

        Args:
            account_id: The account ID
            conversation_id: The conversation ID
            status: New status

        Returns:
            ConversationToggleStatusResponse
        """
        data = {"status": status}
        response = await self._http.post(
            f"/api/v1/accounts/{account_id}/conversations/{conversation_id}/toggle_status",
            json=data,
        )
        return ConversationToggleStatusResponse(**response)

    async def get_counts(
        self,
        account_id: int,
        status: str = "open",
        **filters: Any,
    ) -> dict:
        """Get conversation counts (async).

        Args:
            account_id: The account ID
            status: Status to count
            **filters: Additional filters

        Returns:
            Dictionary with conversation counts
        """
        params = {"status": status, **filters}
        response = await self._http.get(
            f"/api/v1/accounts/{account_id}/conversations/meta",
            params=params,
        )
        return response if isinstance(response, dict) else {}
