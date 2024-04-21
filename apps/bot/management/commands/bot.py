import logging

from django.conf import settings
from django.core.management.base import BaseCommand
from telebot import StateMemoryStorage, TeleBot, custom_filters

from apps.bot import texts
from apps.bot.states import LoginState
from apps.customers.exceptions import CustomerIsAllReadyRegistered, CustomerIsNotRegistered
from apps.customers.services.customers import CustomerService
from apps.customers.utils import login

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

state_storage = StateMemoryStorage()
bot = TeleBot(
    settings.TELEGRAM_BOT_TOKEN,
    state_storage=state_storage,
    num_threads=settings.TELEGRAM_BOT_THREAD_COUNT,
    disable_web_page_preview=True,
)


@bot.message_handler(commands=["start"])
def start_handler(message):
    customer_service = CustomerService()
    customer = customer_service.get(telegram_id=message.chat.id)

    if customer:
        bot.send_message(message.chat.id, texts.ALREADY_ACCOUNT_LOGIN)
    else:
        bot.set_state(message.from_user.id, LoginState.username, message.chat.id)
        bot.send_message(message.chat.id, texts.USERNAME_INPUT_TEXT)


@bot.message_handler(state=LoginState.username)
def get_username_handler(message):
    bot.send_message(message.chat.id, texts.PASSWORD_INPUT_TEXT)
    bot.set_state(message.from_user.id, LoginState.password, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["username"] = message.text


@bot.message_handler(state=LoginState.password)
def get_password_handler(message):
    password = message.text

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        try:
            login(data["username"], password, message.from_user.id)
        except CustomerIsNotRegistered:
            bot.send_message(message.chat.id, texts.ERROR_ACCOUNT_LOGIN)
        except CustomerIsAllReadyRegistered:
            bot.send_message(message.chat.id, texts.ALREADY_ACCOUNT_LOGIN)
        else:
            bot.send_message(message.chat.id, texts.SUCCESS_ACCOUNT_LOGIN)

    bot.delete_state(message.from_user.id, message.chat.id)


class Command(BaseCommand):
    help = "Command to start the bot."

    def handle(self, *args, **kwargs):
        logger.info("Starting bot.")
        bot.add_custom_filter(custom_filters.StateFilter(bot))
        bot.infinity_polling(skip_pending=True)
