from enum import Enum


class Languages(Enum):
    ru = "ru"
    en = "en"

class Menu(Enum):
    info = "info"
    models = "models"
    settings = "settings"

class Models(Enum):
    add = "add"
    list = "list"
    delete = "delete"

class AuthMethod(Enum):
    NONE = "none"
    COOKIES = "cookies"
    HEADERS = "headers"

class Confirmation(Enum):
    """Confirmation options."""
    YES = "yes"
    NO = "no"
