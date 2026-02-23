"""Messages resource for managing conversation messages."""

from __future__ import annotations

from typing import Any

from chatwoot.resources._base import AsyncBaseResource, BaseResource
from chatwoot.types.message import Message


class MessagesResource(BaseResource):
    """Synchronous messages resource."""

    def list(self, account_id: int, conversation_id: int) -> list[Message]:
        """List messages in a conversation.

        Args:
            account_id: The account ID
            conversation_id: The conversation ID

        Returns:
            List of Message objects

        Examples:
            >>> messages = client.messages.list(account_id=1, conversation_id=42)
            ... for msg in messages:
            ... print(msg.content)
        """
        response = self._http.get(
            f"/api/v1/accounts/{account_id}/conversations/{conversation_id}/messages"
        )
        if isinstance(response, list):
            return [Message(**item) for item in response]
        return []

    def create(
        self,
        account_id: int,
        conversation_id: int,
        content: str,
        message_type: str = "outgoing",
        private: bool = False,
        attachments: list[str] | None = None,
        **kwargs: Any,
    ) -> Message:
        """Create/send a message in a conversation.

        Args:
            account_id: The account ID
            conversation_id: The conversation ID
            content: Message content
            message_type: Type of message ('outgoing', 'incoming') (default: 'outgoing')
            private: Whether message is private/internal (default: False)
            attachments: List of file paths to attach (optional)
            **kwargs: Additional message attributes

        Returns:
            Created Message object

        Examples:
            >>> message = client.messages.create(
            ... account_id=1,
            ... conversation_id=42,
            ... content="Hello, how can I help?",
            ... message_type="outgoing",
            ... private=False
            ... )
        """
        data = {
            "content": content,
            "message_type": message_type,
            "private": private,
            **kwargs,
        }

        # Handle file attachments if provided
        if attachments:
            # TODO: Implement multipart file upload
            # For now, just pass the data as JSON
            pass

        response = self._http.post(
            f"/api/v1/accounts/{account_id}/conversations/{conversation_id}/messages",
            json=data,
        )
        return Message(**response)

    def update(
        self, account_id: int, conversation_id: int, message_id: int, content: str
    ) -> Message:
        """Update message content.

        Args:
            account_id: The account ID
            conversation_id: The conversation ID
            message_id: The message ID
            content: New message content

        Returns:
            Updated Message object

        Examples:
            >>> message = client.messages.update(
            ... account_id=1,
            ... conversation_id=42,
            ... message_id=123,
            ... content="Updated message content"
            ... )
        """
        data = {"content": content}
        response = self._http.patch(
            f"/api/v1/accounts/{account_id}/conversations/{conversation_id}/messages/{message_id}",
            json=data,
        )
        return Message(**response)

    def delete(self, account_id: int, conversation_id: int, message_id: int) -> None:
        """Delete a message.

        Args:
            account_id: The account ID
            conversation_id: The conversation ID
            message_id: The message ID

        Examples:
            >>> client.messages.delete(account_id=1, conversation_id=42, message_id=123)
        """
        self._http.delete(
            f"/api/v1/accounts/{account_id}/conversations/{conversation_id}/messages/{message_id}"
        )


class AsyncMessagesResource(AsyncBaseResource):
    """Asynchronous messages resource."""

    async def list(self, account_id: int, conversation_id: int) -> list[Message]:
        """List messages in a conversation (async).

        Args:
            account_id: The account ID
            conversation_id: The conversation ID

        Returns:
            List of Message objects
        """
        response = await self._http.get(
            f"/api/v1/accounts/{account_id}/conversations/{conversation_id}/messages"
        )
        if isinstance(response, list):
            return [Message(**item) for item in response]
        return []

    async def create(
        self,
        account_id: int,
        conversation_id: int,
        content: str,
        message_type: str = "outgoing",
        private: bool = False,
        attachments: list[str] | None = None,
        **kwargs: Any,
    ) -> Message:
        """Create/send a message in a conversation (async).

        Args:
            account_id: The account ID
            conversation_id: The conversation ID
            content: Message content
            message_type: Type of message
            private: Whether message is private
            attachments: List of file paths to attach
            **kwargs: Additional message attributes

        Returns:
            Created Message object
        """
        data = {
            "content": content,
            "message_type": message_type,
            "private": private,
            **kwargs,
        }

        # Handle file attachments if provided
        if attachments:
            # TODO: Implement multipart file upload
            pass

        response = await self._http.post(
            f"/api/v1/accounts/{account_id}/conversations/{conversation_id}/messages",
            json=data,
        )
        return Message(**response)

    async def update(
        self, account_id: int, conversation_id: int, message_id: int, content: str
    ) -> Message:
        """Update message content (async).

        Args:
            account_id: The account ID
            conversation_id: The conversation ID
            message_id: The message ID
            content: New message content

        Returns:
            Updated Message object
        """
        data = {"content": content}
        response = await self._http.patch(
            f"/api/v1/accounts/{account_id}/conversations/{conversation_id}/messages/{message_id}",
            json=data,
        )
        return Message(**response)

    async def delete(
        self, account_id: int, conversation_id: int, message_id: int
    ) -> None:
        """Delete a message (async).

        Args:
            account_id: The account ID
            conversation_id: The conversation ID
            message_id: The message ID
        """
        await self._http.delete(
            f"/api/v1/accounts/{account_id}/conversations/{conversation_id}/messages/{message_id}"
        )
