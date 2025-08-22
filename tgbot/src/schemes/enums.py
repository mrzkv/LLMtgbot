from enum import Enum


class Languages(Enum):
    """Avaible Languages"""
    ru = "ru"
    en = "en"

class Menu(Enum):
    """Menu"""
    info = "info"
    models = "models"
    settings = "settings"

class Models(Enum):
    """Menu button Models - Menu.models """
    add = "add"
    list = "list"
    delete = "delete"

class AuthMethod(Enum):
    """Auth Methods for LLM-Agents"""
    NONE = "none"
    COOKIES = "cookies"
    HEADERS = "headers"

class Confirmation(Enum):
    """Confirmation options."""
    YES = "yes"
    NO = "no"
