import uuid
from collections.abc import AsyncGenerator

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sse_starlette.sse import EventSourceResponse

from app.core.user import get_current_user
from app.crud.chat_history import chat_history_crud
from app.db.session import get_async_session
from app.models.user import User
from app.schemas.chat import ChatHistoryResponse, ChatRequest
from app.services.chat_chain import build_chain

router = APIRouter(tags=["Chat"])


@router.post("/", response_class=EventSourceResponse)
async def chat(
    req: ChatRequest,
    db: AsyncSession = Depends(get_async_session),
) -> EventSourceResponse:
    """
    Chat API endpoint that streams response tokens.
    No longer requires authentication and uses a random session ID for anonymous users.
    """
    # Use a random session ID for anonymous users
    session_id = str(uuid.uuid4())
    chain = build_chain(session_id, db)

    async def event_generator() -> AsyncGenerator[dict, None]:
        try:
            async for chunk in chain.astream({"input": req.message}):
                if "response" in chunk:
                    yield {"event": "message", "data": chunk["response"]}
        except Exception as exc:
            yield {"event": "error", "data": str(exc)}
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    return EventSourceResponse(event_generator())


@router.get("/history", response_model=ChatHistoryResponse)
async def get_chat_history(
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
) -> ChatHistoryResponse:
    """
    Retrieves chat history for the current user.
    """
    messages = await chat_history_crud.get_by_session_id(db, session_id=str(current_user.id), limit=limit)
    return ChatHistoryResponse(messages=messages)


@router.delete("/history", status_code=204)
async def clear_chat_history(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
) -> None:
    """
    Clears all chat history for the current user.
    """
    await chat_history_crud.clear_session_history(db, session_id=str(current_user.id))
