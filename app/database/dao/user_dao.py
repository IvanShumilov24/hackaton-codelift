from sqlalchemy import select, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.user import User
from app.utils.logger import logger


class UserDAO:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_id(self, user_id: int) -> User | None:
        try:
            query = select(User).where(User.id == user_id)
            result = await self.session.execute(query)
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при получении пользователя {user_id}: {e}")
            await self.session.rollback()
            raise

    async def create_user(
            self,
            **user_data: dict,
    ) -> User:
        try:
            user = User(**user_data)
            self.session.add(user)
            await self.session.commit()
            logger.info(f"Создан пользователь: {user.id}")
            return user
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при создании пользователя: {e}")
            await self.session.rollback()
            raise

    async def get_or_create_user(self, user_data: dict) -> tuple[User, bool]:
        user = await self.get_user_by_id(user_data['id'])
        if user:
            return user, False
        try:
            user = await self.create_user(user_data)
            return user, True
        except Exception as e:
            logger.error(f"Ошибка при получении или создании пользователя: {e}")
            raise
