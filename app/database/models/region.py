import uuid

from sqlalchemy import UUID, JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.models.base import Base


class Region(Base):
    __tablename__ = 'regions'

    region_id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, index=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    list: Mapped[list] = mapped_column(JSON, nullable=True)
