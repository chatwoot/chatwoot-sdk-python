"""Contacts resource for managing contacts."""

from __future__ import annotations

from typing import Any

from chatwoot.resources._base import AsyncBaseResource, BaseResource
from chatwoot.types.contact import Contact, ContactCreateResponse
from chatwoot.types.conversation import Conversation
from chatwoot.types.note import Note


class ContactLabelsResource(BaseResource):
    """Nested resource for managing contact labels."""

    def list(self, account_id: int, contact_id: int) -> list[str]:
        """List contact labels.

        Args:
            account_id: The account ID
            contact_id: The contact ID

        Returns:
            List of label strings

        Examples:
             >>> labels = client.contacts.labels.list(account_id=1, contact_id=100)
        """
        response = self._http.get(
            f"/api/v1/accounts/{account_id}/contacts/{contact_id}/labels"
        )
        if isinstance(response, dict) and "payload" in response:
            return response["payload"]
        return response if isinstance(response, list) else []

    def add(self, account_id: int, contact_id: int, labels: list[str]) -> list[str]:
        """Add/replace labels on contact.

        IMPORTANT: This overwrites existing labels, does not append.

        Args:
            account_id: The account ID
            contact_id: The contact ID
            labels: List of label strings to set

        Returns:
            Updated list of labels

        Examples:
             >>> labels = client.contacts.labels.add(
             ... account_id=1,
             ... contact_id=100,
             ... labels=["vip", "priority"]
             ... )
        """
        data = {"labels": labels}
        response = self._http.post(
            f"/api/v1/accounts/{account_id}/contacts/{contact_id}/labels",
            json=data,
        )
        if isinstance(response, dict) and "payload" in response:
            return response["payload"]
        return response if isinstance(response, list) else []


class AsyncContactLabelsResource(AsyncBaseResource):
    """Async nested resource for managing contact labels."""

    async def list(self, account_id: int, contact_id: int) -> list[str]:
        """List contact labels (async).

        Args:
            account_id: The account ID
            contact_id: The contact ID

        Returns:
            List of label strings
        """
        response = await self._http.get(
            f"/api/v1/accounts/{account_id}/contacts/{contact_id}/labels"
        )
        if isinstance(response, dict) and "payload" in response:
            return response["payload"]
        return response if isinstance(response, list) else []

    async def add(
        self, account_id: int, contact_id: int, labels: list[str]
    ) -> list[str]:
        """Add/replace labels on contact (async).

        IMPORTANT: This overwrites existing labels, does not append.

        Args:
            account_id: The account ID
            contact_id: The contact ID
            labels: List of label strings to set

        Returns:
            Updated list of labels
        """
        data = {"labels": labels}
        response = await self._http.post(
            f"/api/v1/accounts/{account_id}/contacts/{contact_id}/labels",
            json=data,
        )
        if isinstance(response, dict) and "payload" in response:
            return response["payload"]
        return response if isinstance(response, list) else []


class ContactNotesResource(BaseResource):
    """Nested resource for managing contact notes."""

    def list(self, account_id: int, contact_id: int) -> list[Note]:
        """List notes on a contact.

        Args:
            account_id: The account ID
            contact_id: The contact ID

        Returns:
            List of Note objects

        Examples:
             >>> notes = client.contacts.notes.list(account_id=1, contact_id=100)
             ... for note in notes:
             ...     print(note.id, note.content)
        """
        response = self._http.get(
            f"/api/v1/accounts/{account_id}/contacts/{contact_id}/notes"
        )
        if isinstance(response, list):
            return [Note(**item) for item in response]
        if isinstance(response, dict) and "payload" in response:
            return [Note(**item) for item in response["payload"]]
        return []

    def get(self, account_id: int, contact_id: int, note_id: int) -> Note:
        """Get a single note on a contact.

        Args:
            account_id: The account ID
            contact_id: The contact ID
            note_id: The note ID

        Returns:
            Note object

        Examples:
             >>> note = client.contacts.notes.get(
             ...     account_id=1, contact_id=100, note_id=7
             ... )
        """
        response = self._http.get(
            f"/api/v1/accounts/{account_id}/contacts/{contact_id}/notes/{note_id}"
        )
        return Note(**response)

    def create(self, account_id: int, contact_id: int, content: str) -> Note:
        """Create a note on a contact.

        Args:
            account_id: The account ID
            contact_id: The contact ID
            content: Note content

        Returns:
            Created Note object

        Examples:
             >>> note = client.contacts.notes.create(
             ...     account_id=1,
             ...     contact_id=100,
             ...     content="Followed up via email"
             ... )
        """
        data = {"note": {"content": content}}
        response = self._http.post(
            f"/api/v1/accounts/{account_id}/contacts/{contact_id}/notes",
            json=data,
        )
        return Note(**response)

    def update(
        self, account_id: int, contact_id: int, note_id: int, content: str
    ) -> Note:
        """Update a note on a contact.

        Args:
            account_id: The account ID
            contact_id: The contact ID
            note_id: The note ID
            content: Updated note content

        Returns:
            Updated Note object

        Examples:
             >>> note = client.contacts.notes.update(
             ...     account_id=1,
             ...     contact_id=100,
             ...     note_id=7,
             ...     content="Updated note text"
             ... )
        """
        data = {"note": {"content": content}}
        response = self._http.patch(
            f"/api/v1/accounts/{account_id}/contacts/{contact_id}/notes/{note_id}",
            json=data,
        )
        return Note(**response)

    def delete(self, account_id: int, contact_id: int, note_id: int) -> None:
        """Delete a note on a contact.

        Args:
            account_id: The account ID
            contact_id: The contact ID
            note_id: The note ID

        Examples:
             >>> client.contacts.notes.delete(
             ...     account_id=1, contact_id=100, note_id=7
             ... )
        """
        self._http.delete(
            f"/api/v1/accounts/{account_id}/contacts/{contact_id}/notes/{note_id}"
        )


class AsyncContactNotesResource(AsyncBaseResource):
    """Async nested resource for managing contact notes."""

    async def list(self, account_id: int, contact_id: int) -> list[Note]:
        """List notes on a contact (async).

        Args:
            account_id: The account ID
            contact_id: The contact ID

        Returns:
            List of Note objects
        """
        response = await self._http.get(
            f"/api/v1/accounts/{account_id}/contacts/{contact_id}/notes"
        )
        if isinstance(response, list):
            return [Note(**item) for item in response]
        if isinstance(response, dict) and "payload" in response:
            return [Note(**item) for item in response["payload"]]
        return []

    async def get(self, account_id: int, contact_id: int, note_id: int) -> Note:
        """Get a single note on a contact (async).

        Args:
            account_id: The account ID
            contact_id: The contact ID
            note_id: The note ID

        Returns:
            Note object
        """
        response = await self._http.get(
            f"/api/v1/accounts/{account_id}/contacts/{contact_id}/notes/{note_id}"
        )
        return Note(**response)

    async def create(self, account_id: int, contact_id: int, content: str) -> Note:
        """Create a note on a contact (async).

        Args:
            account_id: The account ID
            contact_id: The contact ID
            content: Note content

        Returns:
            Created Note object
        """
        data = {"note": {"content": content}}
        response = await self._http.post(
            f"/api/v1/accounts/{account_id}/contacts/{contact_id}/notes",
            json=data,
        )
        return Note(**response)

    async def update(
        self, account_id: int, contact_id: int, note_id: int, content: str
    ) -> Note:
        """Update a note on a contact (async).

        Args:
            account_id: The account ID
            contact_id: The contact ID
            note_id: The note ID
            content: Updated note content

        Returns:
            Updated Note object
        """
        data = {"note": {"content": content}}
        response = await self._http.patch(
            f"/api/v1/accounts/{account_id}/contacts/{contact_id}/notes/{note_id}",
            json=data,
        )
        return Note(**response)

    async def delete(self, account_id: int, contact_id: int, note_id: int) -> None:
        """Delete a note on a contact (async).

        Args:
            account_id: The account ID
            contact_id: The contact ID
            note_id: The note ID
        """
        await self._http.delete(
            f"/api/v1/accounts/{account_id}/contacts/{contact_id}/notes/{note_id}"
        )


class ContactsResource(BaseResource):
    """Synchronous contacts resource."""

    def __init__(self, http):
        """Initialize contacts resource with nested labels and notes resources."""
        super().__init__(http)
        self.labels = ContactLabelsResource(http)
        self.notes = ContactNotesResource(http)

    def list(self, account_id: int, page: int = 1) -> list[Contact]:
        """List contacts with pagination.

        Args:
            account_id: The account ID
            page: Page number (default: 1)

        Returns:
            List of Contact objects

        Examples:
             >>> contacts = client.contacts.list(account_id=1, page=1)
             ... for contact in contacts:
             ... print(contact.name, contact.email)
        """
        params = {"page": page}
        response = self._http.get(
            f"/api/v1/accounts/{account_id}/contacts", params=params
        )
        if isinstance(response, list):
            return [Contact(**item) for item in response]
        return []

    def search(self, account_id: int, query: str) -> list[Contact]:
        """Search contacts.

        Args:
            account_id: The account ID
            query: Search query string

        Returns:
            List of matching Contact objects

        Examples:
             >>> contacts = client.contacts.search(account_id=1, query="john@example.com")
        """
        params = {"q": query}
        response = self._http.get(
            f"/api/v1/accounts/{account_id}/contacts/search", params=params
        )
        if isinstance(response, list):
            return [Contact(**item) for item in response]
        return []

    def get(self, account_id: int, contact_id: int) -> Contact:
        """Get contact details.

        Args:
            account_id: The account ID
            contact_id: The contact ID

        Returns:
            Contact object

        Examples:
             >>> contact = client.contacts.get(account_id=1, contact_id=100)
        """
        response = self._http.get(
            f"/api/v1/accounts/{account_id}/contacts/{contact_id}"
        )
        return Contact(**response)

    def create(
        self,
        account_id: int,
        inbox_id: int,
        **kwargs: Any,
    ) -> ContactCreateResponse:
        """Create a new contact.

        Args:
            account_id: The account ID
            inbox_id: The inbox ID to associate contact with
            **kwargs: Contact attributes (name, email, phone_number, etc.)

        Returns:
            ContactCreateResponse with contact and contact_inbox

        Examples:
             >>> result = client.contacts.create(
             ... account_id=1,
             ... inbox_id=5,
             ... name="John Doe",
             ... email="john@example.com",
             ... )
             ... print(result.contact.id, result.contact_inbox.source_id)
        """
        data = {"inbox_id": inbox_id, **kwargs}
        response = self._http.post(f"/api/v1/accounts/{account_id}/contacts", json=data)
        return ContactCreateResponse(**response)

    def update(
        self,
        account_id: int,
        contact_id: int,
        **kwargs: Any,
    ) -> Contact:
        """Update contact.

        Args:
            account_id: The account ID
            contact_id: The contact ID
            **kwargs: Contact attributes to update

        Returns:
            Updated Contact object

        Examples:
             >>> contact = client.contacts.update(
             ... account_id=1,
             ... contact_id=100,
             ... name="Jane Doe",
             ... custom_attributes={"plan": "premium"}
             ... )
        """
        response = self._http.patch(
            f"/api/v1/accounts/{account_id}/contacts/{contact_id}",
            json=kwargs,
        )
        return Contact(**response)

    def delete(self, account_id: int, contact_id: int) -> None:
        """Delete contact.

        Args:
            account_id: The account ID
            contact_id: The contact ID

        Examples:
             >>> client.contacts.delete(account_id=1, contact_id=100)
        """
        self._http.delete(f"/api/v1/accounts/{account_id}/contacts/{contact_id}")

    def conversations(self, account_id: int, contact_id: int) -> list[Conversation]:
        """Get contact conversations.

        Args:
            account_id: The account ID
            contact_id: The contact ID

        Returns:
            List of Conversation objects for this contact

        Examples:
             >>> conversations = client.contacts.conversations(account_id=1, contact_id=100)
        """
        response = self._http.get(
            f"/api/v1/accounts/{account_id}/contacts/{contact_id}/conversations"
        )
        if isinstance(response, list):
            return [Conversation(**item) for item in response]
        return []

    def merge(
        self, account_id: int, base_contact_id: int, mergee_contact_id: int
    ) -> Contact:
        """Merge two contacts. The mergee is deleted; the base contact is kept.

        Args:
            account_id: The account ID
            base_contact_id: ID of the contact that remains after the merge
            mergee_contact_id: ID of the contact that is merged in and deleted

        Returns:
            The resulting merged Contact object

        Examples:
            >>> contact = client.contacts.merge(
            ...     account_id=1,
            ...     base_contact_id=100,
            ...     mergee_contact_id=200
            ... )
        """
        data = {
            "base_contact_id": base_contact_id,
            "mergee_contact_id": mergee_contact_id,
        }
        response = self._http.post(
            f"/api/v1/accounts/{account_id}/actions/contact_merge",
            json=data,
        )
        return Contact(**response)

    def contactable_inboxes(self, account_id: int, contact_id: int) -> list[dict]:
        """Get inboxes that a contact can be reached through.

        Args:
            account_id: The account ID
            contact_id: The contact ID

        Returns:
            List of dicts with 'source_id' and 'inbox' keys

        Examples:
             >>> inboxes = client.contacts.contactable_inboxes(account_id=1, contact_id=100)
             ... for item in inboxes:
             ...     print(item["source_id"], item["inbox"]["name"])
        """
        response = self._http.get(
            f"/api/v1/accounts/{account_id}/contacts/{contact_id}/contactable_inboxes"
        )
        if isinstance(response, dict) and "payload" in response:
            return response["payload"]
        return response if isinstance(response, list) else []


class AsyncContactsResource(AsyncBaseResource):
    """Asynchronous contacts resource."""

    def __init__(self, http):
        """Initialize async contacts resource with nested labels and notes resources."""
        super().__init__(http)
        self.labels = AsyncContactLabelsResource(http)
        self.notes = AsyncContactNotesResource(http)

    async def list(self, account_id: int, page: int = 1) -> list[Contact]:
        """List contacts with pagination (async).

        Args:
            account_id: The account ID
            page: Page number

        Returns:
            List of Contact objects
        """
        params = {"page": page}
        response = await self._http.get(
            f"/api/v1/accounts/{account_id}/contacts", params=params
        )
        if isinstance(response, list):
            return [Contact(**item) for item in response]
        return []

    async def search(self, account_id: int, query: str) -> list[Contact]:
        """Search contacts (async).

        Args:
            account_id: The account ID
            query: Search query string

        Returns:
            List of matching Contact objects
        """
        params = {"q": query}
        response = await self._http.get(
            f"/api/v1/accounts/{account_id}/contacts/search", params=params
        )
        if isinstance(response, list):
            return [Contact(**item) for item in response]
        return []

    async def get(self, account_id: int, contact_id: int) -> Contact:
        """Get contact details (async).

        Args:
            account_id: The account ID
            contact_id: The contact ID

        Returns:
            Contact object
        """
        response = await self._http.get(
            f"/api/v1/accounts/{account_id}/contacts/{contact_id}"
        )
        return Contact(**response)

    async def create(
        self,
        account_id: int,
        inbox_id: int,
        **kwargs: Any,
    ) -> ContactCreateResponse:
        """Create a new contact (async).

        Args:
            account_id: The account ID
            inbox_id: The inbox ID
            **kwargs: Contact attributes

        Returns:
            ContactCreateResponse with contact and contact_inbox
        """
        data = {"inbox_id": inbox_id, **kwargs}
        response = await self._http.post(
            f"/api/v1/accounts/{account_id}/contacts", json=data
        )
        return ContactCreateResponse(**response)

    async def update(
        self,
        account_id: int,
        contact_id: int,
        **kwargs: Any,
    ) -> Contact:
        """Update contact (async).

        Args:
            account_id: The account ID
            contact_id: The contact ID
            **kwargs: Contact attributes to update

        Returns:
            Updated Contact object
        """
        response = await self._http.patch(
            f"/api/v1/accounts/{account_id}/contacts/{contact_id}",
            json=kwargs,
        )
        return Contact(**response)

    async def delete(self, account_id: int, contact_id: int) -> None:
        """Delete contact (async).

        Args:
            account_id: The account ID
            contact_id: The contact ID
        """
        await self._http.delete(f"/api/v1/accounts/{account_id}/contacts/{contact_id}")

    async def conversations(
        self, account_id: int, contact_id: int
    ) -> list[Conversation]:
        """Get contact conversations (async).

        Args:
            account_id: The account ID
            contact_id: The contact ID

        Returns:
            List of Conversation objects
        """
        response = await self._http.get(
            f"/api/v1/accounts/{account_id}/contacts/{contact_id}/conversations"
        )
        if isinstance(response, list):
            return [Conversation(**item) for item in response]
        return []

    async def merge(
        self, account_id: int, base_contact_id: int, mergee_contact_id: int
    ) -> Contact:
        """Merge two contacts (async). The mergee is deleted; the base is kept.

        Args:
            account_id: The account ID
            base_contact_id: ID of the contact that remains after the merge
            mergee_contact_id: ID of the contact that is merged in and deleted

        Returns:
            The resulting merged Contact object
        """
        data = {
            "base_contact_id": base_contact_id,
            "mergee_contact_id": mergee_contact_id,
        }
        response = await self._http.post(
            f"/api/v1/accounts/{account_id}/actions/contact_merge",
            json=data,
        )
        return Contact(**response)

    async def contactable_inboxes(self, account_id: int, contact_id: int) -> list[dict]:
        """Get inboxes that a contact can be reached through (async).

        Args:
            account_id: The account ID
            contact_id: The contact ID

        Returns:
            List of dicts with 'source_id' and 'inbox' keys
        """
        response = await self._http.get(
            f"/api/v1/accounts/{account_id}/contacts/{contact_id}/contactable_inboxes"
        )
        if isinstance(response, dict) and "payload" in response:
            return response["payload"]
        return response if isinstance(response, list) else []
