"""Common types and enums used across resources."""

from enum import Enum

from pydantic import BaseModel


class Unset:
    """Sentinel for a value not provided."""


UNSET = Unset()


class ConversationStatus(str, Enum):
    """Status of a conversation."""

    OPEN = "open"
    RESOLVED = "resolved"
    PENDING = "pending"
    SNOOZED = "snoozed"


class MessageType(str, Enum):
    """Type of message."""

    INCOMING = "incoming"
    OUTGOING = "outgoing"
    ACTIVITY = "activity"
    TEMPLATE = "template"


class MessageContentType(str, Enum):
    """Content type of message."""

    TEXT = "text"
    INPUT_TEXT = "input_text"
    INPUT_TEXTAREA = "input_textarea"
    INPUT_EMAIL = "input_email"
    INPUT_SELECT = "input_select"
    CARDS = "cards"
    FORM = "form"
    ARTICLE = "article"


class AgentRole(str, Enum):
    """Role of an agent in the account."""

    AGENT = "agent"
    ADMINISTRATOR = "administrator"


class AvailabilityStatus(str, Enum):
    """Availability status of an agent."""

    ONLINE = "online"
    BUSY = "busy"
    OFFLINE = "offline"


class ConversationPriority(str, Enum):
    """Priority of a conversation."""

    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class ChannelType(str, Enum):
    """Type of inbox channel."""

    WEB_WIDGET = "web_widget"
    API = "api"
    EMAIL = "email"
    FACEBOOK = "facebook"
    TWITTER = "twitter"
    WHATSAPP = "whatsapp"
    SMS = "sms"
    TELEGRAM = "telegram"
    LINE = "line"


class PaginationMeta(BaseModel):
    """Metadata for paginated responses."""

    mine_count: int | None = None
    unassigned_count: int | None = None
    assigned_count: int | None = None
    all_count: int | None = None
    current_page: int | None = None
