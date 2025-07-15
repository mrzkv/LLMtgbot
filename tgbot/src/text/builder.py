from aiogram.utils.markdown import link

from src.core.ModelGateway.ai_http_client import HTTPMethods
from src.schemes.enums import AuthMethod, Languages, Menu


class TextBuilder:
    """
    Class for building text messages for bot
    with different languages, using MarkdownV2.
     """

    def __init__(self, language: Languages) -> None:
        if not isinstance(language, Languages):
            raise TypeError("Language must be an instance of Languages Enum.")
        self._language = language

    @staticmethod
    def start_handler() -> str:
        return "🌐:"

    def main_menu_greeting(self) -> str:
        if self._language == Languages.en:
            return "You are in the *main menu*\\. Here's what you can do\\:"
        if self._language == Languages.ru:
            return "Вы в *главном меню*\\. Вот что вы можете сделать\\:"
        raise ValueError(f"Invalid language: {self._language.value}")

    def main( # noqa: PLR0911
            self,
            item: Menu,
    ) -> str:
        if not isinstance(item, Menu):
            raise TypeError("Item must be an instance of Menu Enum.")

        if self._language == Languages.en:
            if item == Menu.info:
                return (
                    "Information about bot\\:\n\n"
                    f"Source code: {link('github.com/mrzkv/LLMtgbot', 'https://github.com/mrzkv/LLMtgbot')}\n"
                    f"Creator: {link('tg.mrzkv.ru', 'https://tg.mrzkv.ru')}\n\n"
                )
            if item == Menu.models:
                return "You are in the *Models menu* 🧠"
            if item == Menu.settings:
                return "You are in the *Bot settings* ⚙️"
            return "Unknown menu item. Please select an option from the menu below."

        if self._language == Languages.ru:
            if item == Menu.info:
                return (
                    "Информация о боте\\:\n\n"
                    f"Исходный код: {link('github.com/mrzkv/LLMtgbot', 'https://github.com/mrzkv/LLMtgbot')}\n"
                    f"Создатель: {link('tg.mrzkv.ru', 'https://tg.mrzkv.ru')}\n\n"
                )
            if item == Menu.models:
                return "Вы в *меню моделей* 🧠"
            if item == Menu.settings:
                return "Вы в *настройках бота* ⚙️"
            return "Неизвестный пункт меню\\. Пожалуйста, выберите опцию из меню ниже\\."

        raise ValueError(f"Invalid language: {self._language.value}")

    def add_ai_url(self) -> str:
        if self._language == Languages.en:
            return "Please enter the AI URL \\(up to its endpoint\\)\\.\nExample: `https://example.com/ai/v5/chat/`"
        if self._language == Languages.ru:
            return "Пожалуйста, введите ссылку на AI \\(до её эндпоинта\\)\\.\nПример: `https://example.com/ai/v5/chat/`"
        raise ValueError(f"Invalid language: {self._language.value}")

    def choose_http_method_prompt(self) -> str:
        """Returns the prompt to choose an HTTP method (GET, POST, PUT, PATCH, DELETE)."""
        if self._language == Languages.en:
            return "Now, please choose the *HTTP method* to use for this AI\\."
        if self._language == Languages.ru:
            return "Теперь, пожалуйста, выберите *HTTP\\-метод* для этого AI\\."
        raise ValueError(f"Invalid language: {self._language.value}")

    def choose_auth_method_prompt(self) -> str:
        """Returns the prompt to choose an authentication method (None, Cookies, Headers)."""
        if self._language == Languages.en:
            return "Next, choose the *authentication method*\\."
        if self._language == Languages.ru:
            return "Далее, выберите *метод аутентификации*\\."
        raise ValueError(f"Invalid language: {self._language.value}")

    def enter_auth_data_prompt(self, auth_method: AuthMethod) -> str:
        """
        Returns the prompt for entering authentication data,
        specifying the expected format for headers or cookies.
        """
        example_header = "X\\-Auth\\-Token ASsdfjsdkfjskdfj"
        example_cookie = "sessionid=somevalue"

        if self._language == Languages.en:
            if auth_method == AuthMethod.HEADERS:
                return (
                    "Please enter the *header key and value* separated by a space\\.\n"
                    f"Example: `{example_header}`"
                )
            if auth_method == AuthMethod.COOKIES:
                return (
                    "Please enter the *cookie key and value* separated by an equals sign\\.\n"
                    f"Example: `{example_cookie}`" # Cookies typically use key=value
                )
            # Should not happen if AuthMethod.NONE is handled by UI not calling this.
            return "Please enter authentication data\\."

        if self._language == Languages.ru:
            if auth_method == AuthMethod.HEADERS:
                return (
                    "Пожалуйста, введите *ключ и значение заголовка*, разделенные пробелом\\.\n"
                    f"Пример: `{example_header}`"
                )
            if auth_method == AuthMethod.COOKIES:
                return (
                    "Пожалуйста, введите *ключ и значение куки*, разделенные знаком равенства\\.\n"
                    f"Пример: `{example_cookie}`"
                )
            return "Пожалуйста, введите данные аутентификации\\."

        raise ValueError(f"Invalid language: {self._language.value}")

    def confirm_ai_config_prompt(
            self,
            url: str,
            http_method: HTTPMethods,
            auth_method: AuthMethod,
            auth_data: str | None = None,  # Key-value pair Cookie/Header
    ) -> str:
        """
        Returns the confirmation message displaying all entered AI configuration details.
        """
        confirm_text_en = "Please confirm the following AI configuration\\:"
        confirm_text_ru = "Пожалуйста, подтвердите следующую конфигурацию AI\\:"

        url_line_en = f"URL: `{url}`"
        url_line_ru = f"URL: `{url}`"

        method_line_en = f"HTTP Method: *{http_method.value}*"
        method_line_ru = f"HTTP Метод: *{http_method.value}*"

        auth_method_line_en = f"Authentication: *{auth_method.value.capitalize()}*"
        auth_method_line_ru = f"Аутентификация: *{auth_method.value.capitalize()}*"

        auth_data_line_en = ""
        auth_data_line_ru = ""
        if auth_method != AuthMethod.NONE and auth_data:
            auth_data_line_en = f"Auth Data: `{auth_data}`"
            auth_data_line_ru = f"Данные аутентификации: `{auth_data}`"

        if self._language == Languages.en:
            return (
                f"{confirm_text_en}\n"
                f"{url_line_en}\n"
                f"{method_line_en}\n"
                f"{auth_method_line_en}\n"
                f"{auth_data_line_en}\n"
                "\nIs this correct\\?"
            )
        if self._language == Languages.ru:
            return (
                f"{confirm_text_ru}\n"
                f"{url_line_ru}\n"
                f"{method_line_ru}\n"
                f"{auth_method_line_ru}\n"
                f"{auth_data_line_ru}\n"
                "\nВерно\\?"
            )

        raise ValueError(f"Invalid language: {self._language.value}")



    def list_ai_models(self) -> str:
        if self._language == Languages.en:
            return "Here is your *list of AI models*\\."
        if self._language == Languages.ru:
            return "Вот ваш *список моделей ИИ*\\."
        return "..."

    def delete_ai_prompt(self) -> str:
        if self._language == Languages.en:
            return "Please select the *AI to delete*\\."
        if self._language == Languages.ru:
            return "Пожалуйста, выберите *ИИ для удаления*\\."
        return "..."

    def invalid_url(self) -> str:
        if self._language == Languages.en:
            return "Invalid URL ❌"
        if self._language == Languages.ru:
            return "Неправильная ссылка ❌"
        return "..."

    def invalid_auth_creds(self, auth_method: AuthMethod) -> str:
        if self._language == Languages.en:
            return f"Invalid credentials for {auth_method.value}\\."
        if self._language == Languages.ru:
            if auth_method == AuthMethod.HEADERS:
                return "Некорректные данные для Заголовка\\."
            return "Некорректные данные для Куки\\."
        return "..."
