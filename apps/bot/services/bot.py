import logging
from dataclasses import dataclass

from telebot import TeleBot
from telebot.types import InputMediaPhoto
from telebot.util import antiflood

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class BotSenderService:
    bot: TeleBot

    @staticmethod
    def _group_media_files(photos, message):
        media = [InputMediaPhoto(photo_ulr, parse_mode="HTML") for photo_ulr in photos]
        media[0].caption = message[0:1024]
        return media

    def send_media(self, chat_id: int, message: str, photos: list[str]) -> list[str]:
        media = self._group_media_files(photos, message)

        result = antiflood(self.bot.send_media_group, chat_id, number_retries=2, media=media)

        photo_ids = [photo_media.photo[-1].file_id for photo_media in result]
        return photo_ids

    def send(self, chat_id: int, message: str):
        antiflood(self.bot.send_message, chat_id, number_retries=2, text=message[:4096], parse_mode="HTML")


def split_message(text, max_length=4096):
    parts = []
    while len(text) > max_length:
        split_point = text.rfind("\n", 0, max_length)
        if split_point == -1:
            split_point = max_length
        parts.append(text[:split_point])
        text = text[split_point:]
    parts.append(text)
    return parts
