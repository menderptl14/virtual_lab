import uuid
from datetime import datetime
from enum import Enum
from sqlalchemy import String, Text, DateTime, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column
from infrastructure.database.connection import Base


class LabDifficulty(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class LabStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class Lab(Base):
    __tablename__ = "labs"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    difficulty: Mapped[LabDifficulty] = mapped_column(SAEnum(LabDifficulty), nullable=False)
    status: Mapped[LabStatus] = mapped_column(SAEnum(LabStatus), default=LabStatus.DRAFT)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def publish(self) -> None:
        """Domain behaviour: only DRAFT labs can be published."""
        if self.status != LabStatus.DRAFT:
            raise ValueError(f"Cannot publish a lab with status '{self.status}'.")
        self.status = LabStatus.PUBLISHED

    def archive(self) -> None:
        self.status = LabStatus.ARCHIVED
