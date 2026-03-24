from typing import List
from uuid import UUID, uuid4
from domain.lab.models.entities import Lab, LabDifficulty, LabStatus
from domain.lab.repositories.base import ILabRepository
from core.exceptions import NotFoundException


class LabService:
    """
    Orchestrates lab use cases.
    Depends on the repository interface — not the DB implementation.
    """

    def __init__(self, repo: ILabRepository):
        self.repo = repo

    async def create_lab(self, title: str, description: str, difficulty: LabDifficulty) -> Lab:
        lab = Lab(
            id=uuid4(),
            title=title,
            description=description,
            difficulty=difficulty,
        )
        return await self.repo.save(lab)

    async def get_lab(self, lab_id: UUID) -> Lab:
        lab = await self.repo.get_by_id(lab_id)
        if not lab:
            raise NotFoundException(f"Lab '{lab_id}' not found.")
        return lab

    async def list_labs(self) -> List[Lab]:
        return await self.repo.list_all()

    async def publish_lab(self, lab_id: UUID) -> Lab:
        lab = await self.get_lab(lab_id)
        lab.publish()  # Domain method enforces invariant
        return await self.repo.save(lab)

    async def archive_lab(self, lab_id: UUID) -> Lab:
        lab = await self.get_lab(lab_id)
        lab.archive()
        return await self.repo.save(lab)
