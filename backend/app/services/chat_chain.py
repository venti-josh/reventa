from fastapi import Depends
from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory, PostgresChatMessageHistory
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.session import get_async_session


def _memory_for(user_id: str, db: AsyncSession) -> ConversationBufferMemory:
    """Create memory instance based on settings configuration."""
    if settings.CHAT_MEMORY_TYPE == "postgres":
        # For Postgres, we need to convert the session to a connection string
        # Ensure the table exists and has correct schema:
        # id SERIAL PRIMARY KEY, session_id TEXT, message JSONB
        connection_string = str(db.get_bind().engine.url)

        return ConversationBufferMemory(
            memory_key="history",
            return_messages=True,
            chat_memory=PostgresChatMessageHistory(
                connection_string=connection_string,
                table_name="chat_history",
                session_id=user_id,
            ),
        )
    return ConversationBufferMemory(return_messages=True, memory_key="history")


def build_chain(user_id: str, db: AsyncSession = Depends(get_async_session)) -> ConversationChain:
    """Build a conversation chain with the appropriate memory and LLM."""
    memory = _memory_for(user_id, db)
    llm = ChatOpenAI(
        streaming=True,
        temperature=0.2,
        model_name=settings.CHAT_MODEL,
        openai_api_key=settings.OPENAI_API_KEY,
    )
    return ConversationChain(llm=llm, memory=memory, verbose=False)
