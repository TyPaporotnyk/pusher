import logging

from telebot import TeleBot

from apps.bot.utils import send_message
from apps.bot.utils.new import get_new_group_adverts
from apps.bot.utils.text import get_advert_text
from apps.customers.services.customers import CustomerService
from apps.customers.services.real_estate import RealEstateService

logger = logging.getLogger(__name__)


def broadcast_group(bot: TeleBot):
    customer_service = CustomerService()
    real_estate_service = RealEstateService()

    # Берем последний элемент в базе под тегом группа
    last_group_advert = real_estate_service.get_last("group")
    last_real_estate_id = last_group_advert.real_estate_id if last_group_advert else 0

    # Получаем список элементов по айди последней добавленной недвижимости в базе
    new_group_adverts = get_new_group_adverts(last_real_estate_id)
    new_group_adverts.reverse()
    new_group_adverts = new_group_adverts[0:50]

    logger.info(f"New group adverts received: {len(new_group_adverts)}")
    send_count = 0
    for group_advert in new_group_adverts:
        advert_group_name = group_advert[5]
        images = group_advert[4].split(",")[:10]
        advert_message = group_advert[0]
        advert_id = group_advert[1]
        advert_link = group_advert[6]

        message_template = get_advert_text(advert_message, advert_link)
        # Добавляем пост о недвижимости в базу данных и помечаем как группу
        advert = real_estate_service.get_or_create(advert_id, "group")

        # Получаем юзеров для рассылки
        users = customer_service.get_all_by_group(advert_group_name)
        for user in users:
            # Проверка на наличие группы в выбранных у юзера
            if advert in user.real_estates.all():
                continue

            # Проверка на наличие выбранных ключевых слов юзера в сообщении объявления
            user_groups_keywords = user.groups_keywords.all()
            if user_groups_keywords:
                groups_keywords_in_advert_message = any(
                    [user_groups_keyword.name in advert_message for user_groups_keyword in user_groups_keywords]
                )

                if not groups_keywords_in_advert_message:
                    continue

            try:
                send_message(bot, user.telegram_id, message_template, images)
            except Exception as e:
                logger.info(f"Error broadcasting advert to user {user.telegram_id}: {repr(e)}")
            else:
                # Добавляем недвижимость к юзеру
                user.real_estates.add(advert)
                user.save()

                logger.debug(f"Broadcasting advert to user {user.telegram_id} success")

        send_count += 1
    logger.info(f"Success send count: {send_count}")


# def broadcast_keyword(bot: TeleBot):
#     customer_service = CustomerService()
#     real_estate_service = RealEstateService()
#     new_group_adverts = get_new_group_adverts()
#
#     # Убрать
#     new_group_adverts = new_group_adverts[0:50]
#
#     for group_advert in new_group_adverts:
#         advert_group_name = group_advert[5]
#         images = group_advert[4].split(",")[:10]
#         advert_message = group_advert[0]
#         advert_id = group_advert[1]
#
#         # Добавляем пост о недвижимости в базу данных
#         advert = real_estate_service.get_or_create(advert_id, "group")
#
#         # Получаем юзеров для рассылки
#         users = customer_service.get_all_by_group(advert_group_name)
#         for user in users:
#             if advert in user.real_estates.all():
#                 continue
#
#             try:
#                 send_message(bot, user.telegram_id, advert_message, images)
#             except Exception as e:
#                 logger.info(f"Error broadcasting advert to user {user.telegram_id}: {repr(e)}")
#             else:
#                 # Добавляем недвижимость к юзеру
#                 user.real_estates.add(advert)
#                 user.save()
#                 logger.info(f"Broadcasting advert to user {user.telegram_id} success")
