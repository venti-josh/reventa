from typing import Literal

from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str


class ChatMessage(BaseModel):
    """Schema for individual chat messages in JSON format"""

    type: Literal["human", "ai", "system"]
    data: dict[str, str]


class ChatHistoryItem(BaseModel):
    """Schema for chat history items from DB"""

    id: int
    session_id: str
    message: ChatMessage

    model_config = {"from_attributes": True}


class ChatHistoryResponse(BaseModel):
    """Schema for chat history response"""

    messages: list[ChatHistoryItem]
