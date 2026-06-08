"""Type definitions for contact notes."""

from datetime import datetime

from pydantic import BaseModel


class Note(BaseModel):
    """Contact note."""

    id: int
    content: str
    contact_id: int | None = None
    user_id: int | None = None
    account_id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
