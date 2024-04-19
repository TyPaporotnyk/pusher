from telebot.handler_backends import State, StatesGroup


class LoginState(StatesGroup):
    username = State()
    password = State()
