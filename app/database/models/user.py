from typing import Optional

from pydantic.v1 import UUID4
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base, mapped_column, Mapped

from app.database.models.base import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    first_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    last_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)