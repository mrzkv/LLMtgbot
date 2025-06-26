from datetime import UTC, datetime

from aiogram.types import CallbackQuery, Message, User

from src.core.db.pool import sqlite_pool
from src.repository.user import UserRepository
from src.tables.telegram_users import TelegramUserDTO, TelegramUserInputDTO


class UserService:
    """Service for work with users"""
    def __init__(
        self,
        user: User,
        repo: UserRepository,
    ) -> None:
        self._user = user
        self._repo = repo

    async def add_new_user(self) -> None:
        user_input_dto = TelegramUserInputDTO(
            user_id=self._user.id,
            first_name=self._user.first_name,
            last_name=self._user.last_name,
            language_code=self._user.language_code,
            is_bot=self._user.is_bot,
            username=self._user.username,
            added_date=datetime.now(UTC).isoformat(),
        )

        db_user: TelegramUserDTO | None = await self._repo.get(user_id=self._user.id)

        if not db_user:
            await self._repo.add(user_input_dto)
            await self._repo.commit()
        else:
            user_dto: TelegramUserDTO = TelegramUserDTO.from_input(
                row_id=db_user.id,
                input_dto=user_input_dto,
            )
            if db_user != user_dto:
                await self._repo.update(user_dto)
                await self._repo.commit()

        # Create Keyboards


class UserServiceFactory:
    """UserService factory"""
    @staticmethod
    async def create(event: Message | CallbackQuery) -> UserService:
        if isinstance(event, (CallbackQuery, Message)):
            user = event.from_user
        else:
            raise TypeError(f"Unsupported event: {type(event)}")

        async with sqlite_pool.get_async_session() as session:
            repo = UserRepository(session)
            return UserService(user, repo)
