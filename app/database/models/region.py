from sqlalchemy import JSON, String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.database.models.base import Base


class Region(Base):
    __tablename__ = 'regions'

    region_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    list: Mapped[list] = mapped_column(JSON, nullable=True)
