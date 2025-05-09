from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.chat_history import ChatHistory


class CRUDChatHistory(CRUDBase[ChatHistory, dict, dict]):
    """CRUD operations for chat history with revised schema."""

    async def get_by_session_id(self, db: AsyncSession, *, session_id: str, limit: int = 100) -> Sequence[ChatHistory]:
        """Get chat history for a specific session."""
        query = select(ChatHistory).where(ChatHistory.session_id == session_id).order_by(ChatHistory.id).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()

    async def clear_session_history(self, db: AsyncSession, *, session_id: str) -> None:
        """Delete all chat history for a specific session."""
        query = select(ChatHistory).where(ChatHistory.session_id == session_id)
        result = await db.execute(query)
        items = result.scalars().all()
        for item in items:
            await db.delete(item)
        await db.commit()

    async def add_message(self, db: AsyncSession, *, session_id: str, role: str, content: str) -> ChatHistory:
        """Add a new message to the chat history."""
        chat_message = ChatHistory(session_id=session_id, message={"type": role, "data": {"content": content}})
        db.add(chat_message)
        await db.commit()
        await db.refresh(chat_message)
        return chat_message


# Create a singleton instance
chat_history_crud = CRUDChatHistory(ChatHistory)
