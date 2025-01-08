from aiogram.fsm.state import State, StatesGroup


class BotScheme(StatesGroup):
    main_menu = State()
    # create_new_order = State() кажется не нужен
    create_inn_payer = State()
    create_inn_recipient = State()
    create_sum_order = State()
    create_date_order = State()
