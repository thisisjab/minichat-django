from enum import Enum

from pydantic import BaseModel


class MessageType(str, Enum):
    PRIVATE_TEXT_MESSAGE = "private_text_message"
    ERROR = "error"


class BaseSchema(BaseModel):
    """Base schema for all ws requests."""

    type: MessageType


class PrivateTextMessageSchema(BaseSchema):
    """Schema for sending private text message ws request."""

    body: str
    receiver: str
