from aiogram.types import CallbackQuery, Message, User

from src.core.db.pool import sqlite_pool
from src.core.ModelGateway.ai_http_client import HTTPMethods
from src.repository.llm import LLMRepository
from src.repository.user import UserRepository
from src.schemes.enums import AuthMethod
from src.tables.integration_ai import IntegrationAIDTO, IntegrationAIInputDTO


class LLMService:
    def __init__(
            self,
            llm_repo: LLMRepository,
            user_repo: UserRepository,
            user: User,
    ) -> None:
        self.llm_repo = llm_repo
        self.user_repo = user_repo
        self.user = user


    async def add_new_ai(
            self,
            ai_url: str,
            http_method: HTTPMethods,
            auth_method: AuthMethod,
            auth_creds: str | None = None,
    ) -> IntegrationAIDTO:

        if http_method == HTTPMethods.GET:
            http_method_value = 0
        elif http_method == HTTPMethods.POST:
            http_method_value = 1
        elif http_method == HTTPMethods.PUT:
            http_method_value = 2
        elif http_method == HTTPMethods.DELETE:
            http_method_value = 3
        elif http_method == HTTPMethods.PATCH:
            http_method_value = 4
        else:
            raise TypeError("Unexpected HTTPMethod")

        if auth_method == AuthMethod.NONE:
            auth_method_value = 0
        elif auth_method == AuthMethod.COOKIES:
            auth_method_value = 1
        elif auth_method == AuthMethod.HEADERS:
            auth_method_value = 2
        else:
            raise TypeError("Unexpected AuthMethod")


        return await self.llm_repo.add(
            dto=IntegrationAIInputDTO(
                creator_id=self.user.id,
                url=ai_url,
                http_method=http_method_value,
                auth_type=auth_method_value,
                auth_creds=auth_creds,
            ),
        )



class LLMServiceFactory:
    @staticmethod
    def create(event: Message | CallbackQuery) -> LLMService:
        if isinstance(event, (CallbackQuery, Message)):
            user: User = event.from_user
        else:
            raise TypeError(f"Unsupported event: {type(event)}")

        session_generator = sqlite_pool.get_async_session

        user_repo = UserRepository(session_generator)
        llm_repo = LLMRepository(session_generator)
        return LLMService(llm_repo, user_repo, user)
