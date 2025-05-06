from fastapi import APIRouter

from app.routers import (
    auth,
    events,
    org_domains,
    public,
    stats,
    survey_instances,
    surveys,
)

api_router = APIRouter(prefix="/api/v1")

# Include all routers
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(org_domains.router, prefix="/org/domains", tags=["organization domains"])
api_router.include_router(events.router, prefix="/events", tags=["events"])
api_router.include_router(surveys.router, prefix="/surveys", tags=["surveys"])
api_router.include_router(survey_instances.router, prefix="/survey-instances", tags=["survey instances"])
api_router.include_router(public.router, prefix="/l", tags=["public"])
api_router.include_router(stats.router, tags=["stats"])
