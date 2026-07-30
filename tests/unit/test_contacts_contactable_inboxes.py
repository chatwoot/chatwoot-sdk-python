"""Tests for contacts.contactable_inboxes method."""

import pytest
from unittest.mock import AsyncMock

from chatwoot.resources.contacts import ContactsResource, AsyncContactsResource


CONTACTABLE_INBOXES_PAYLOAD = [
    {
        "source_id": "abc-123",
        "inbox": {
            "id": 5,
            "name": "Support Inbox",
            "channel_type": "Channel::Api",
            "channel_id": 3,
            "avatar_url": "",
            "provider": None,
        },
    },
    {
        "source_id": "def-456",
        "inbox": {
            "id": 6,
            "name": "Web Inbox",
            "channel_type": "Channel::WebWidget",
            "channel_id": 4,
            "avatar_url": "",
            "provider": None,
        },
    },
]


def test_contactable_inboxes_returns_empty_on_non_list(mock_http):
    """Test contactable_inboxes returns empty list for a non-list response."""
    mock_http.get.return_value = {}

    resource = ContactsResource(mock_http)
    result = resource.contactable_inboxes(account_id=1, contact_id=100)

    assert result == []


def test_contactable_inboxes_with_list_response(mock_http):
    """Test contactable_inboxes handles bare list response."""
    mock_http.get.return_value = CONTACTABLE_INBOXES_PAYLOAD

    resource = ContactsResource(mock_http)
    result = resource.contactable_inboxes(account_id=1, contact_id=100)

    mock_http.get.assert_called_once_with(
        "/api/v1/accounts/1/contacts/100/contactable_inboxes"
    )
    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0]["source_id"] == "abc-123"
    assert result[0]["inbox"]["id"] == 5
    assert result[0]["inbox"]["name"] == "Support Inbox"
    assert result[1]["source_id"] == "def-456"
    assert result[1]["inbox"]["channel_type"] == "Channel::WebWidget"


@pytest.mark.asyncio
async def test_async_contactable_inboxes(mock_async_http):
    """Test async contactable_inboxes returns bare list response."""
    mock_async_http.get = AsyncMock(return_value=CONTACTABLE_INBOXES_PAYLOAD)

    resource = AsyncContactsResource(mock_async_http)
    result = await resource.contactable_inboxes(account_id=1, contact_id=100)

    mock_async_http.get.assert_called_once_with(
        "/api/v1/accounts/1/contacts/100/contactable_inboxes"
    )
    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0]["source_id"] == "abc-123"


@pytest.mark.asyncio
async def test_async_contactable_inboxes_empty(mock_async_http):
    """Test async contactable_inboxes returns empty list on empty response."""
    mock_async_http.get = AsyncMock(return_value={})

    resource = AsyncContactsResource(mock_async_http)
    result = await resource.contactable_inboxes(account_id=1, contact_id=100)

    assert result == []
