from aiogram.fsm.state import State, StatesGroup


class BotScheme(StatesGroup):
    no_user_name = State()
    main_menu = State()
    # create_new_order = State() кажется не нужен
    input_inn_payer = State()
    input_inn_recipient = State()
    input_sum_order = State()
    input_date_order = State()
