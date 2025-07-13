from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.keyboards.decoder import (
    AICallback,
    BackCallback,
    LanguageCallback,
    MenuCallback,
)
from src.schemes.enums import Languages, Menu, Models


class InlineKeyboardFactory:
    """Factory for creating inline keyboards"""
    def __init__(
            self,
            language: Languages,
    ) -> None:
        if not isinstance(language, Languages):
            raise TypeError("Language must be an instance of Languages Enum.")
        self._language = language
        self._builder = InlineKeyboardBuilder()

    @staticmethod
    def choose_language() -> InlineKeyboardMarkup:
        """Create inline keyboard for choosing language"""
        builder = InlineKeyboardBuilder()
        builder.button(text="🇷🇺 Русский", callback_data=LanguageCallback(language=Languages.ru).pack())
        builder.button(text="🇺🇸 English", callback_data=LanguageCallback(language=Languages.en).pack())
        builder.adjust(2)
        return builder.as_markup()


    def main_menu(self) -> InlineKeyboardMarkup:
        """Create inline keyboard for main menu"""
        if self._language == Languages.ru:
            self._builder.button(
                text="🧠 Модели",
                callback_data=MenuCallback(item="models", language=self._language).pack(),
            )
            self._builder.button(
                text="ℹ️ Информация", # noqa: RUF001
                callback_data=MenuCallback(item="info", language=self._language).pack(),
            )
            self._builder.button(
                text="⚙️ Настройки",
                callback_data=MenuCallback(item="settings", language=self._language).pack(),
            )
        elif self._language == Languages.en:
            self._builder.button(
                text="🧠 Models",
                callback_data=MenuCallback(item="models", language=self._language).pack(),
            )
            self._builder.button(
                text="ℹ️ Information", # noqa: RUF001
                callback_data=MenuCallback(item="info", language=self._language).pack(),
            )
            self._builder.button(
                text="⚙️ Settings",
                callback_data=MenuCallback(item="settings", language=self._language).pack(),
            )
        self._builder.adjust(1)
        return self._builder.as_markup()

    def main(
            self,
            item: Menu,
    ) -> InlineKeyboardMarkup:
        if not isinstance(item, Menu):
            raise TypeError("Item must be an instance of Menu Enum.")


        if self._language == Languages.ru:
            if item == Menu.info:
                self._builder.button(
                    text="↩️ Назад в меню",
                    callback_data=BackCallback(language=self._language).pack(),
                )
                self._builder.adjust(1)
            elif item == Menu.models:
                self._builder.button(
                    text="➕ Добавить ИИ", # noqa: RUF001
                    callback_data=AICallback(action=Models.add, language=self._language).pack(),
                )
                self._builder.button(
                    text="🗑️ Удалить ИИ",
                    callback_data=AICallback(action=Models.delete, language=self._language).pack(),
                )
                self._builder.button(
                    text="📋 Список ИИ",
                    callback_data=AICallback(action=Models.list, language=self._language).pack(),
                )
                self._builder.button(
                    text="↩️ Назад в меню",
                    callback_data=BackCallback(language=self._language).pack(),
                )
                self._builder.adjust(2, 1, 1) # Изменено для расположения кнопок
            elif item == Menu.settings:
                self._builder.button(
                    text="↩️ Назад в меню",
                    callback_data=BackCallback(language=self._language).pack(),
                )
                self._builder.adjust(1)
            else:
                return self.main_menu()

        elif self._language == Languages.en:
            if item == Menu.info:
                self._builder.button(
                    text="↩️ Back to menu",
                    callback_data=BackCallback(language=self._language).pack(),
                )
                self._builder.adjust(1)
            elif item == Menu.models:
                self._builder.button(
                    text="➕ Add AI", # noqa: RUF001
                    callback_data=AICallback(action=Models.add, language=self._language).pack(),
                )
                self._builder.button(
                    text="🗑️ Delete AI",
                    callback_data=AICallback(action=Models.delete, language=self._language).pack(),
                )
                self._builder.button(
                    text="📋 List AI",
                    callback_data=AICallback(action=Models.list, language=self._language).pack(),
                )
                self._builder.button(
                    text="↩️ Back to menu",
                    callback_data=BackCallback(language=self._language).pack(),
                )
                self._builder.adjust(2, 1, 1) # Изменено для расположения кнопок
            elif item == Menu.settings:
                self._builder.button(
                    text="↩️ Back to menu",
                    callback_data=BackCallback(language=self._language).pack(),
                )
                self._builder.adjust(1)
            else:
                return self.main_menu()

        return self._builder.as_markup()
