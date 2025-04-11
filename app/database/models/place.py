import uuid

from sqlalchemy import UUID, ForeignKey, String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.database.models.base import Base


class Place(Base):
    __tablename__ = "places"

    place_id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, index=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    region_id: Mapped[int] = mapped_column(Integer, ForeignKey("regions.region_id", ondelete="CASCADE"))
