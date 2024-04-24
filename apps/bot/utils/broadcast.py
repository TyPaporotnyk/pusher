import logging
from abc import abstractmethod
from dataclasses import dataclass

from django.conf import settings
from telebot import TeleBot

from apps.bot.services.facebook import FacebookBaseRepository
from apps.bot.utils import send_message
from apps.bot.utils.text import get_advert_text
from apps.customers.models.keywords import Keyword
from apps.customers.services.customers import CustomerService
from apps.customers.services.real_estate import RealEstateService

logger = logging.getLogger(__name__)


def is_message_contain_keywords(user_keywords: list[Keyword], message: str) -> bool:
    is_any_keyword_in_message = any([user_keyword.name in message for user_keyword in user_keywords])
    return not user_keywords or is_any_keyword_in_message


@dataclass(kw_only=True)
class BaseBroadcasterService:
    facebook_service: FacebookBaseRepository
    customer_service: CustomerService
    real_estate_service: RealEstateService
    bot: TeleBot

    @abstractmethod
    def broadcast(self):
        pass


@dataclass(kw_only=True)
class GroupBroadcasterService(BaseBroadcasterService):

    def broadcast(self):
        send_cont = 0
        last_group_advert_id = self.real_estate_service.get_last_id_by_tag("group")
        new_group_adverts = self.facebook_service.get_new_adverts(last_group_advert_id)
        new_group_adverts.reverse()
        new_group_adverts = new_group_adverts[: settings.MAX_POSTS_PER_TIME]
        logger.info(f"Adverts received: {len(new_group_adverts)}")

        for group_advert in new_group_adverts:
            message_template = get_advert_text(group_advert.message, group_advert.post_link)
            advert = self.real_estate_service.get_or_create(group_advert.id, "group")
            users = self.customer_service.get_all_by_group_url(group_advert.group_link)
            advert_images = group_advert.attachments[: settings.MAX_IMAGES_PER_POST]

            for user in users:
                # Проверка на то есть ли выбранный заказ у пользователя
                # или не содержит ли сообщение ключевые слова пользователя
                if user.is_advert_contains(advert) or not is_message_contain_keywords(
                    user.groups_keywords.all(), message_template
                ):
                    continue

                send_message(self.bot, user.telegram_id, message_template, advert_images)
                user.add_advert(advert)
                send_cont += 1

        logger.info(f"Adverts sent count: {send_cont}")


@dataclass(kw_only=True)
class KeywordBroadcasterService(BaseBroadcasterService):

    def broadcast(self):
        sent_count = 0
        last_keyword_advert_id = self.real_estate_service.get_last_id_by_tag("keyword")
        new_keyword_adverts = self.facebook_service.get_new_adverts(last_keyword_advert_id)
        new_keyword_adverts.reverse()
        new_keyword_adverts = new_keyword_adverts[: settings.MAX_POSTS_PER_TIME]
        logger.info(f"New keyword adverts received: {len(new_keyword_adverts)}")

        for keyword_advert in new_keyword_adverts:
            message_template = get_advert_text(keyword_advert.message, keyword_advert.post_link)
            advert = self.real_estate_service.get_or_create(keyword_advert.id, "keyword")
            users = self.customer_service.get_all_by_keyword(keyword_advert.key)
            advert_images = keyword_advert.attachments[: settings.MAX_IMAGES_PER_POST]

            for user in users:
                if user.is_advert_contains(advert):
                    continue

                send_message(self.bot, user.telegram_id, message_template, advert_images)
                user.add_advert(advert)
                sent_count += 1

        logger.info(f"Success send count: {sent_count}")
