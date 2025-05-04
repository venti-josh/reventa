from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.user import user_crud
from app.db.session import get_db
from app.schemas.user import UserCreate, UserRead, UserUpdate

router = APIRouter()


@router.get("/", response_model=list[UserRead])
async def read_users(
    db: AsyncSession = Depends(get_db), skip: int = 0, limit: int = 100
) -> list[UserRead]:
    users = await user_crud.get_multi(db, skip=skip, limit=limit)
    return users


@router.post("/", response_model=UserRead)
async def create_user(
    *,
    user_in: UserCreate,
    db: AsyncSession = Depends(get_db),
) -> UserRead:
    user = await user_crud.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    user = await user_crud.create(db, obj_in=user_in)
    return user


@router.get("/{user_id}", response_model=UserRead)
async def read_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
) -> UserRead:
    user = await user_crud.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )
    return user


@router.put("/{user_id}", response_model=UserRead)
async def update_user(
    *,
    user_id: int,
    user_in: UserUpdate,
    db: AsyncSession = Depends(get_db),
) -> UserRead:
    user = await user_crud.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )
    user = await user_crud.update(db, db_obj=user, obj_in=user_in)
    return user


@router.delete("/{user_id}", response_model=UserRead)
async def delete_user(
    *,
    user_id: int,
    db: AsyncSession = Depends(get_db),
) -> UserRead:
    user = await user_crud.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )
    user = await user_crud.remove(db, id=user_id)
    return user
