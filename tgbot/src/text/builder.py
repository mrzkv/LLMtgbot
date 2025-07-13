from aiogram.utils.markdown import link

from src.schemes.enums import Languages, Menu


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
                    "Информация о боте\\:\n\n" # noqa: RUF001
                    f"Исходный код: {link('github.com/mrzkv/LLMtgbot', 'https://github.com/mrzkv/LLMtgbot')}\n"
                    f"Создатель: {link('tg.mrzkv.ru', 'https://tg.mrzkv.ru')}\n\n"
                )
            if item == Menu.models:
                return "Вы в *меню моделей* 🧠"
            if item == Menu.settings:
                return "Вы в *настройках бота* ⚙️"
            return "Неизвестный пункт меню\\. Пожалуйста, выберите опцию из меню ниже\\."

        raise ValueError(f"Invalid language: {self._language.value}")

    def add_ai_prompt(self) -> str:
        if self._language == Languages.en:
            return "Please enter the *details for adding AI*\\."
        if self._language == Languages.ru:
            return "Пожалуйста, введите *данные для добавления ИИ*\\."
        return "..."

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
