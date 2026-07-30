"""Type definitions for contacts."""

from datetime import datetime

from pydantic import BaseModel, Field


class InboxSlim(BaseModel):
    """
    A data object that contains only partial information of an Inbox. This is attached to the Contact object because, when you reference
    an Inbox through Contact, this is all the data it contains.

    eg. client.contacts.search(...) -> response JSON = {
        id: 123,
        ...
        contact_inboxes: [
            {
                source_id: "+15551234567",
                inbox: {
                    id: 789,
                    avatar_url: "https://cdn.example.com/inbox-avatar.png",
                    channel_id: 42,
                    name: "Foo",
                    channel_type: "Channel::Whatsapp",
                    provider: "whatsapp_cloud"
                }
            }
        ]
    }
    """

    id: int
    channel_id: int
    name: str
    channel_type: str
    avatar_url: str | None = None
    provider: str | None = None


class ContactInbox(BaseModel):
    """Contact's inbox association."""

    source_id: str
    inbox_id: int | None = Field(
        default=None,
        deprecated="inbox_id is deprecated; use inbox.id instead.",
    )
    inbox: InboxSlim


class Contact(BaseModel):
    """Contact information."""

    id: int
    name: str | None = None
    email: str | None = None
    phone_number: str | None = None
    identifier: str | None = None
    thumbnail: str | None = None
    avatar_url: str | None = None
    additional_attributes: dict = Field(default_factory=dict)
    custom_attributes: dict = Field(default_factory=dict)
    contact_inboxes: list[ContactInbox] = Field(default_factory=list)
    last_activity_at: datetime | None = None
    created_at: datetime | None = None
    availability_status: str | None = None
    blocked: bool = False


class ContactCreateResponse(BaseModel):
    """Response from creating a contact."""

    contact: Contact
    contact_inbox: ContactInbox
