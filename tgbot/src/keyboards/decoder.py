from aiogram.filters.callback_data import CallbackData

from src.schemes.enums import Languages, Menu, Models


class LanguageCallback(CallbackData, prefix="lang"):
    language: Languages

class MenuCallback(CallbackData, prefix="menu"):
    item: Menu
    language: Languages

class AICallback(CallbackData, prefix="ai"):
    action: Models
    language: Languages

class BackCallback(CallbackData, prefix="back"):
    language: Languages
