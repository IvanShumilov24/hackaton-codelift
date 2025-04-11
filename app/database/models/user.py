from typing import Optional

from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column, Mapped

from app.database.models.base import Base


class User(Base):
    __tablename__ = 'users'

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
