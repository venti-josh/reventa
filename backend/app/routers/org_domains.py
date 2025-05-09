import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.org_allowed_domain import org_allowed_domain_crud
from app.db.session import get_async_session
from app.schemas.org_allowed_domain import OrgAllowedDomainCreate, OrgAllowedDomainRead

router = APIRouter()


@router.get("/", response_model=list[OrgAllowedDomainRead])
async def get_org_domains(
    db: AsyncSession = Depends(get_async_session),
) -> list[OrgAllowedDomainRead]:
    """List allowed email domains for the organization."""
    domains = await org_allowed_domain_crud.get_multi(db)
    return [OrgAllowedDomainRead.model_validate(domain, from_attributes=True) for domain in domains]


@router.post("/", response_model=OrgAllowedDomainRead)
async def create_org_domain(
    *,
    domain_in: OrgAllowedDomainCreate,
    db: AsyncSession = Depends(get_async_session),
) -> OrgAllowedDomainRead:
    """Add a new allowed email domain."""
    domain = await org_allowed_domain_crud.create(db, obj_in=domain_in)
    return OrgAllowedDomainRead.model_validate(domain, from_attributes=True)


@router.delete("/{id}", response_model=OrgAllowedDomainRead)
async def delete_org_domain(
    *,
    id: int,
    db: AsyncSession = Depends(get_async_session),
) -> OrgAllowedDomainRead:
    """Remove an allowed email domain."""
    # Convert integer id to UUID by first converting to string
    try:
        domain_uuid = uuid.UUID(str(id))
        domain = await org_allowed_domain_crud.get(db, id=domain_uuid)
    except ValueError as err:
        raise HTTPException(
            status_code=400,
            detail="Invalid ID format",
        ) from err

    if not domain:
        raise HTTPException(
            status_code=404,
            detail="Domain not found",
        )

    # Use the integer ID for remove since the CRUD expects an int
    domain = await org_allowed_domain_crud.remove(db, id=id)
    return OrgAllowedDomainRead.model_validate(domain, from_attributes=True)
