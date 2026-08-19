# Chatwoot SDK for Python

A modern, type-safe Python SDK for the [Chatwoot](https://www.chatwoot.com/) API. This SDK provides both synchronous and asynchronous interfaces to interact with Chatwoot's REST API, with full type hints for better IDE support and code safety.

## Features

- 🔒 **Type-safe**: Full type hints with Pydantic models
- ⚡ **Async support**: Both sync and async clients available
- 🎯 **Comprehensive**: Covers all major Chatwoot API resources
- 🛡️ **Error handling**: Custom exceptions for different error types

## Installation

```bash
pip install chatwoot-sdk
# or
uv add chatwoot-sdk
```

> **Note:** The PyPI package name is `chatwoot-sdk`. The GitHub repository is named `chatwoot-sdk-python`.

## Quick Start

```python
from chatwoot import ChatwootClient

# Initialize the client
client = ChatwootClient(
    base_url="https://app.chatwoot.com",
    api_token="your_api_token_here"
)

# Fetch your profile
profile = client.profile.get()
print(f"Logged in as: {profile.name}")

# List open conversations
conversations = client.conversations.list(
    account_id=1,
    status="open"
)

# Send a message
message = client.messages.create(
    account_id=1,
    conversation_id=42,
    content="Hello from Python SDK!"
)

# Always close the client when done
client.close()
```

## Usage Examples

### Using Context Manager

```python
from chatwoot import ChatwootClient

with ChatwootClient(base_url="...", api_token="...") as client:
    profile = client.profile.get()
    conversations = client.conversations.list(account_id=1, status="open")
    # Client is automatically closed
```

### Async Usage

```python
import asyncio
from chatwoot import AsyncChatwootClient

async def main():
    async with AsyncChatwootClient(base_url="...", api_token="...") as client:
        profile = await client.profile.get()
        conversations = await client.conversations.list(
            account_id=1,
            status="open"
        )

asyncio.run(main())
```

### Working with Conversations

```python
# List conversations with filters
conversations = client.conversations.list(
    account_id=1,
    status="open",
    assignee_type="me",
    inbox_id=5,
    labels=["urgent", "billing"]
)

# Get conversation details
conversation = client.conversations.get(account_id=1, conversation_id=42)

# Update conversation priority
updated = client.conversations.update(
    account_id=1,
    conversation_id=42,
    priority="high"
)

# Assign conversation to an agent (or pass team_id for a team)
agent = client.conversations.assign(
    account_id=1,
    conversation_id=42,
    assignee_id=10
)

# Change conversation status
status = client.conversations.toggle_status(
    account_id=1,
    conversation_id=42,
    status="resolved"
)

# Add labels to conversation
labels = client.conversations.labels.add(
    account_id=1,
    conversation_id=42,
    labels=["bug", "priority"]
)
```

### Managing Contacts

```python
# Create a contact
contact = client.contacts.create(
    account_id=1,
    inbox_id=5,
    name="John Doe",
    email="john@example.com",
    phone_number="+1234567890"
)

# Search contacts
results = client.contacts.search(account_id=1, query="john@example.com")

# Update contact
contact = client.contacts.update(
    account_id=1,
    contact_id=100,
    name="Jane Doe",
    custom_attributes={"plan": "premium"}
)

# Add labels to contact
labels = client.contacts.labels.add(
    account_id=1,
    contact_id=100,
    labels=["vip", "premium"]
)
```

### Sending Messages

```python
# Send a text message
message = client.messages.create(
    account_id=1,
    conversation_id=42,
    content="Hello! How can I help you?",
    message_type="outgoing"
)

# Send a private note
note = client.messages.create(
    account_id=1,
    conversation_id=42,
    content="Internal note for team",
    message_type="outgoing",
    private=True
)

# Update a message
updated = client.messages.update(
    account_id=1,
    message_id=123,
    content="Updated message content"
)
```

### Managing Teams

```python
# List teams
teams = client.teams.list(account_id=1)

# Create a team
team = client.teams.create(
    account_id=1,
    name="Support Team",
    description="Customer support team"
)

# Add agents to team
client.teams.agents.add(
    account_id=1,
    team_id=5,
    agent_ids=[10, 11, 12]
)

# List team members
members = client.teams.agents.list(account_id=1, team_id=5)
```

### Error Handling

```python
from chatwoot import (
    ChatwootClient,
    ChatwootAuthError,
    ChatwootNotFoundError,
    ChatwootValidationError,
)

client = ChatwootClient(base_url="...", api_token="...")

try:
    conversation = client.conversations.get(account_id=1, conversation_id=999)
except ChatwootAuthError as e:
    print(f"Authentication failed: {e}")
except ChatwootNotFoundError as e:
    print(f"Resource not found: {e}")
except ChatwootValidationError as e:
    print(f"Validation error: {e}")
    if e.errors:
        for error in e.errors:
            print(f"  - {error['field']}: {error['message']}")
```

## API Resources

The SDK provides access to the following Chatwoot API resources:

- **Profile**: User profile information
- **Conversations**: Conversation management and filtering
- **Messages**: Send and manage messages
- **Contacts**: Contact management and search
- **Inboxes**: Inbox configuration
- **Teams**: Team management
- **Agents**: Agent management
- **Labels**: Label management (nested under conversations and contacts)

## Development

### Setup

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync

# Run tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=chatwoot --cov-report=term-missing

# Type check
uvx ty check .

# Lint
uv run ruff check .

# Format code
uv run ruff format .
```

### Project Structure

```
chatwoot-sdk-python/
├── chatwoot/
│   ├── __init__.py           # Public API
│   ├── client.py             # Main client classes
│   ├── exceptions.py         # Custom exceptions
│   ├── _http.py              # HTTP client wrapper
│   ├── types/                # Pydantic models
│   │   ├── common.py
│   │   ├── conversation.py
│   │   ├── message.py
│   │   ├── contact.py
│   │   └── ...
│   └── resources/            # API resource implementations
│       ├── _base.py
│       ├── profile.py
│       ├── conversations.py
│       ├── messages.py
│       └── ...
├── tests/
│   └── unit/
├── examples/
└── README.md
```

## Requirements

- Python 3.11+
- httpx
- pydantic

## License

MIT License - see LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

- [Documentation](https://github.com/chatwoot/chatwoot-sdk-python)
- [Issue Tracker](https://github.com/chatwoot/chatwoot-sdk-python/issues)
- [Chatwoot API Documentation](https://www.chatwoot.com/docs/product/others/api)
