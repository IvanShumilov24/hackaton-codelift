

from app.database.dao.user_dao import UserDAO
from app.database.models.user import User
from app.utils.logger import logger


class UserService:
    def __init__(self, user_dao: UserDAO):
        self.user_dao = user_dao

    async def register_user(self, **user_data) -> User:
        try:
            existing_user = await self.user_dao.get_user_by_id(user_data['id'])
            if existing_user:
                logger.info(f"Пользователь уже существует: {user_data['id']}")
                return existing_user

            user = await self.user_dao.create_user(**user_data)
            logger.success(f"Успешная регистрация: {user.id}")
            return user
        except Exception as e:
            logger.critical(f"Ошибка регистрации пользователя: {e}")
            raise RuntimeError("Ошибка регистрации") from e

    async def get_user_profile(self, user_id: int) -> dict:
        try:
            user = await self.user_dao.get_user_by_id(user_id)
            if not user:
                raise ValueError("Пользователь не найден")

            return {
                'id': user.id,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
            }
        except Exception as e:
            logger.error(f"Ошибка получения профиля {user_id}: {e}")
            raise