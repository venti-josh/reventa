from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.user import get_current_user
from app.crud.organization import organization_crud
from app.db.session import get_async_session
from app.models.user import User
from app.schemas.organization import OrganizationCreate, OrganizationRead, OrganizationUpdate

router = APIRouter()


@router.post("/", response_model=OrganizationRead, status_code=status.HTTP_201_CREATED)
async def create_organization(
    *,
    organization_in: OrganizationCreate,
    db: AsyncSession = Depends(get_async_session),
) -> OrganizationRead:
    """Create a new organization."""
    # Check if an organization with the same name already exists
    existing_org = await organization_crud.get_by_name(db, name=organization_in.name)
    if existing_org:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Organization with this name already exists",
        )

    organization = await organization_crud.create(db, obj_in=organization_in)
    return OrganizationRead.model_validate(organization, from_attributes=True)


@router.get("/", response_model=list[OrganizationRead])
async def list_organizations(
    *,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
) -> list[OrganizationRead]:
    """
    List organizations.

    This endpoint requires authentication and will only return the user's
    own organization.
    """
    # Users can only see their own organization
    if current_user.organization:
        return [OrganizationRead.model_validate(current_user.organization, from_attributes=True)]
    return []


@router.get("/{organization_id}", response_model=OrganizationRead)
async def get_organization(
    *,
    organization_id: UUID,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
) -> OrganizationRead:
    """
    Get a specific organization by ID.

    This endpoint requires authentication and will only return the organization
    if it belongs to the current user.
    """
    organization = await organization_crud.get(db, id=organization_id)
    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found",
        )

    # Check if user has access to this organization
    if not current_user.organization or current_user.organization.id != organization_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to access this organization",
        )

    return OrganizationRead.model_validate(organization, from_attributes=True)


@router.patch("/{organization_id}", response_model=OrganizationRead)
async def update_organization(
    *,
    organization_id: UUID,
    organization_in: OrganizationUpdate,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
) -> OrganizationRead:
    """
    Update an organization.

    This endpoint requires authentication and the user must belong to the organization.
    """
    organization = await organization_crud.get(db, id=organization_id)
    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found",
        )

    # Check if user has access to this organization
    if not current_user.organization or current_user.organization.id != organization_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to update this organization",
        )

    organization = await organization_crud.update(db, db_obj=organization, obj_in=organization_in)
    return OrganizationRead.model_validate(organization, from_attributes=True)


@router.delete("/{organization_id}", response_model=OrganizationRead)
async def delete_organization(
    *,
    organization_id: UUID,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
) -> OrganizationRead:
    """
    Delete an organization.

    This endpoint requires authentication and is currently disabled for all users.
    """
    # Organization deletion is a sensitive operation
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Organization deletion is not permitted",
    )
