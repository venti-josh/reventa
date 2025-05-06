import io

import qrcode
import qrcode.image.svg
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.link import link_crud
from app.crud.survey_instance import survey_instance_crud
from app.db.session import get_async_session
from app.schemas.link import LinkCreate

router = APIRouter()


@router.post("/link", response_model=dict[str, str])
async def create_survey_link(
    *,
    link_in: LinkCreate,
    db: AsyncSession = Depends(get_async_session),
) -> dict[str, str]:
    """Create a link for a survey instance and return the URL and QR code."""
    survey_instance = await survey_instance_crud.get(db, id=link_in.survey_instance_id)

    if not survey_instance:
        raise HTTPException(
            status_code=404,
            detail="Survey instance not found",
        )

    # Create a link for the survey instance
    link = await link_crud.create(db, obj_in=link_in)

    # Generate URL
    url = f"/l/{link.id}"

    # Generate QR code
    factory = qrcode.image.svg.SvgImage
    img = qrcode.make(url, image_factory=factory)

    # Convert QR code to SVG string
    stream = io.BytesIO()
    img.save(stream)
    qr_svg = stream.getvalue().decode()

    return {"url": url, "qr_svg": qr_svg}
