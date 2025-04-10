from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker


class Database:
    def __init__(self, db_url: str):
        self.engine = create_async_engine(db_url)
        self.session_maker = sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )
