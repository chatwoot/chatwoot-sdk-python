"""Type definitions for Chatwoot API resources."""

from chatwoot.types.agent import Agent
from chatwoot.types.common import (
    Unset,
    UNSET,
    AgentRole,
    AvailabilityStatus,
    ChannelType,
    ConversationPriority,
    ConversationStatus,
    MessageContentType,
    MessageType,
    PaginationMeta,
)
from chatwoot.types.contact import Contact, ContactCreateResponse, ContactInbox
from chatwoot.types.conversation import (
    Conversation,
    ConversationAssignee,
    ConversationContact,
    ConversationInbox,
    ConversationMeta,
    ConversationTeam,
    ConversationToggleStatusResponse,
)
from chatwoot.types.inbox import Inbox
from chatwoot.types.label import Label
from chatwoot.types.message import Message, MessageAttachment, MessageSender
from chatwoot.types.profile import Profile, ProfileAccount
from chatwoot.types.team import Team

__all__ = [
    # Enums
    "AgentRole",
    "AvailabilityStatus",
    "ChannelType",
    "ConversationPriority",
    "ConversationStatus",
    "MessageContentType",
    "MessageType",
    # Common
    "Unset",
    "UNSET",
    "PaginationMeta",
    # Agent
    "Agent",
    # Contact
    "Contact",
    "ContactCreateResponse",
    "ContactInbox",
    # Conversation
    "Conversation",
    "ConversationAssignee",
    "ConversationContact",
    "ConversationInbox",
    "ConversationMeta",
    "ConversationTeam",
    "ConversationToggleStatusResponse",
    # Inbox
    "Inbox",
    # Label
    "Label",
    # Message
    "Message",
    "MessageAttachment",
    "MessageSender",
    # Profile
    "Profile",
    "ProfileAccount",
    # Team
    "Team",
]
