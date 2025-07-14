from logging import getLogger

from aiogram import Router
from aiogram.types import CallbackQuery

from src.keyboards.builder import InlineKeyboardFactory
from src.keyboards.callback import BackCallback, LanguageCallback, MenuCallback
from src.text.builder import TextBuilder

router = Router()

logger = getLogger(__name__)

@router.callback_query(LanguageCallback.filter())
async def select_language_handler(
        callback: CallbackQuery,
        callback_data: LanguageCallback,
) -> None:
    selected_language = callback_data.language
    logger.info(f"{callback.from_user.id}: selected language {selected_language.value}")
    await callback.answer()
    await callback.message.edit_text(
        text=TextBuilder(selected_language).main_menu_greeting(),
        reply_markup=InlineKeyboardFactory(selected_language).main_menu(),
    )

@router.callback_query(BackCallback.filter())
async def back_to_menu_handler(callback: CallbackQuery, callback_data: BackCallback) -> None:
    language = callback_data.language
    logger.info(f"{callback.from_user.id}: clicked back to main menu in language '{language.value}'")
    await callback.answer()
    await callback.message.edit_text(
        text=TextBuilder(language).main_menu_greeting(),
        reply_markup=InlineKeyboardFactory(language).main_menu(),
    )

@router.callback_query(MenuCallback.filter())
async def menu_handler(
        callback: CallbackQuery,
        callback_data: MenuCallback,
) -> None:
    selected_item = callback_data.item # 'models', 'info', 'settings'
    selected_language = callback_data.language
    logger.info(
        f"{callback.from_user.id}: selected menu item '{selected_item}' "
        f"in language '{selected_language.value}'", # Используем .value для логирования
    )
    await callback.answer()
    await callback.message.edit_text(
        text = TextBuilder(selected_language).main(selected_item),
        reply_markup = InlineKeyboardFactory(selected_language).main(selected_item),
        disable_web_page_preview = True,
    )
