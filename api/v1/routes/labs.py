from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from domain.lab.models.entities import LabDifficulty
from application.lab.service import LabService
from infrastructure.database.connection import get_db_session
from infrastructure.repositories.lab_repository import LabRepository
from core.exceptions import NotFoundException, not_found

router = APIRouter(prefix="/labs", tags=["Labs"])


# ── Schemas ──────────────────────────────────────────────────────────────────

class CreateLabRequest(BaseModel):
    title: str
    description: str | None = None
    difficulty: LabDifficulty


class LabResponse(BaseModel):
    id: UUID
    title: str
    description: str | None
    difficulty: LabDifficulty
    status: str

    class Config:
        from_attributes = True


# ── Dependency ────────────────────────────────────────────────────────────────

def get_lab_service(db: AsyncSession = Depends(get_db_session)) -> LabService:
    return LabService(repo=LabRepository(db))


# ── Endpoints ─────────────────────────────────────────────────────────────────

@router.post("/", response_model=LabResponse, status_code=status.HTTP_201_CREATED)
async def create_lab(body: CreateLabRequest, service: LabService = Depends(get_lab_service)):
    return await service.create_lab(
        title=body.title,
        description=body.description,
        difficulty=body.difficulty,
    )


@router.get("/", response_model=list[LabResponse])
async def list_labs(service: LabService = Depends(get_lab_service)):
    return await service.list_labs()


@router.get("/{lab_id}", response_model=LabResponse)
async def get_lab(lab_id: UUID, service: LabService = Depends(get_lab_service)):
    try:
        return await service.get_lab(lab_id)
    except NotFoundException:
        raise not_found("Lab", str(lab_id))


@router.patch("/{lab_id}/publish", response_model=LabResponse)
async def publish_lab(lab_id: UUID, service: LabService = Depends(get_lab_service)):
    try:
        return await service.publish_lab(lab_id)
    except NotFoundException:
        raise not_found("Lab", str(lab_id))


@router.patch("/{lab_id}/archive", response_model=LabResponse)
async def archive_lab(lab_id: UUID, service: LabService = Depends(get_lab_service)):
    try:
        return await service.archive_lab(lab_id)
    except NotFoundException:
        raise not_found("Lab", str(lab_id))
