from logging import getLogger

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from src.keyboards.builder import InlineKeyboardFactory
from src.keyboards.callback import AICallback, AuthMethodCallback, HTTPMethodCallback
from src.schemes.enums import AuthMethod, Models
from src.states.ai import AddAIStates
from src.text.builder import TextBuilder
from src.utils.validators.auth_data import AuthDataValidator
from src.utils.validators.url import URLValidator

router = Router()

logger = getLogger(__name__)

@router.callback_query(AICallback.filter(F.action == Models.add))
async def handle_add_ai_start(
        callback: CallbackQuery,
        callback_data: AICallback,
        state: FSMContext,
) -> None:
    selected_language = callback_data.language
    await callback.answer()
    await callback.message.edit_text(
        text = TextBuilder(selected_language).add_ai_url(),
        reply_markup=None,
    )
    await state.update_data(language=selected_language)
    await state.set_state(AddAIStates.waiting_for_url)

@router.message(AddAIStates.waiting_for_url)
async def handle_ai_url_input(
        message: Message,
        state: FSMContext,
) -> None:
    language = await state.get_value("language")
    user_url = message.text
    text_builder = TextBuilder(language)
    if URLValidator().is_valid(user_url):
       await state.update_data(ai_url=user_url)
       await state.set_state(AddAIStates.waiting_for_http_method)
       text = text_builder.choose_http_method_prompt()
       reply_markup = InlineKeyboardFactory(language).choose_http_method()
    else:
        text = text_builder.invalid_url()
        reply_markup = None

    await message.answer(
        text=text,
        reply_markup=reply_markup,
    )

@router.callback_query(
    HTTPMethodCallback.filter(),
    AddAIStates.waiting_for_http_method,
)
async def handle_http_method_choice(
    callback: CallbackQuery,
    callback_data: HTTPMethodCallback,
    state: FSMContext,
) -> None:
    await callback.answer()
    await state.update_data(http_method=callback_data.method)
    await state.set_state(AddAIStates.waiting_for_auth_method)
    selected_language = callback_data.language
    await callback.message.edit_text(
        text=TextBuilder(selected_language).choose_auth_method_prompt(),
        reply_markup=InlineKeyboardFactory(selected_language).choose_auth_method(),
    )


@router.callback_query(
    AuthMethodCallback.filter(),
    AddAIStates.waiting_for_auth_method,
)
async def handle_auth_method_choice(
        callback: CallbackQuery,
        callback_data: AuthMethodCallback,
        state: FSMContext,
) -> None:
    auth_method = callback_data.method
    language = callback_data.language
    keyboard_factory = InlineKeyboardFactory(language)
    text_builder = TextBuilder(language)
    await callback.answer()

    if auth_method == AuthMethod.NONE:
        await state.update_data(auth_data=None)

        state_user_data = await state.get_data()
        text = text_builder.confirm_ai_config_prompt(
            url = state_user_data.get("ai_url"),
            http_method = state_user_data.get("http_method"),
            auth_data = state_user_data.get("auth_data"),
            auth_method = state_user_data.get("auth_method"),
        )
        reply_markup = keyboard_factory.confirm_config()
        await state.set_state(AddAIStates.confirming_config)
    else:
        await state.update_data(auth_method=auth_method)
        text=text_builder.enter_auth_data_prompt(auth_method)
        reply_markup=None
        await state.set_state(AddAIStates.waiting_for_auth_data)
    await callback.message.edit_text(
        text=text,
        reply_markup=reply_markup,
        disable_web_page_preview=True,
    )

@router.message(AddAIStates.waiting_for_auth_data)
async def handle_auth_data_input(
        message: Message,
        state: FSMContext,
) -> None:
    auth_data_input = message.text
    auth_method = await state.get_value("auth_method")
    language = await state.get_value("language")
    keyboard_factory = InlineKeyboardFactory(language)
    text_builder = TextBuilder(language)

    if AuthDataValidator(auth_data_input).validate(auth_method):
        user_data = await state.get_data()

        ai_url = user_data.get("ai_url")
        http_method = user_data.get("http_method")
        auth_data = auth_data_input
        text = text_builder.confirm_ai_config_prompt(
            url = ai_url,
            http_method=http_method,
            auth_method=auth_method,
            auth_data = auth_data,
        )
        reply_markup = keyboard_factory.confirm_config()
        await state.set_state(AddAIStates.confirming_config)
        await state.update_data(auth_data=auth_data)

    else:
        text = text_builder.invalid_auth_creds(auth_method)
        reply_markup = None

    await message.answer(
        text=text,
        reply_markup=reply_markup,
    )
