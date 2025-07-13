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
