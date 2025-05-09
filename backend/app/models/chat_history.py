from sqlalchemy import JSON, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base


class ChatHistory(Base):
    """
    Model for storing chat history messages.
    Compatible with LangChain's PostgresChatMessageHistory.

    Schema follows LangChain's requirements:
    - id: auto-incrementing integer primary key
    - session_id: text identifier for the conversation
    - message: JSON data containing the message (role, content)
    """

    __tablename__ = "chat_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    session_id: Mapped[str] = mapped_column(String, index=True, nullable=False)
    message: Mapped[dict] = mapped_column(JSON, nullable=False)
