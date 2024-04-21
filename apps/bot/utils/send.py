import logging

from telebot import TeleBot

from apps.bot.services.bot import BotSenderService

logger = logging.getLogger(__name__)


def send_message(bot: TeleBot, user_id: int, message: str, photos: list[str]) -> bool:
    sender_service = BotSenderService(bot)

    if photos:
        try:
            sender_service.send_media(user_id, message, photos)
        except Exception as e:
            logger.warning("Error sending message to bot due to %s", str(e))
            sender_service.send(user_id, message)
            return True
    else:
        sender_service.send(user_id, message)
        return True
