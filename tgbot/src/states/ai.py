from aiogram.fsm.state import State, StatesGroup


class AddAIStates(StatesGroup):
    """
    States for the "Add AI" wizard.
    """
    waiting_for_url = State()
    waiting_for_http_method = State()
    waiting_for_auth_method = State()
    waiting_for_auth_data = State()
    confirming_config = State()
