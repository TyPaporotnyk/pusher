from django.conf import settings
from telebot import TeleBot

from apps.base.services.bot import BotSenderService, send_message
from apps.customers.repository import CustomerRepository
from apps.customers.services import CustomerService
from apps.filters.services.customer import CustomerPostMatchFilter
from apps.posts.repository import PostRepository
from apps.posts.utils.template import get_message_text
from config.celery import app


@app.task
def link_post_to_users(post_id: int):
    post_repository = PostRepository()
    customer_service = CustomerService(customer_repository=CustomerRepository())

    post = post_repository.get(id=post_id)
    customers = customer_service.get_active_customers()

    for customer in customers:
        match_filter = CustomerPostMatchFilter(customer)

        if match_filter.is_valid(post):
            customer.matched_posts.add(post)
            customer.save()

            if customer.telegram_id:
                send_message_to_telegram.delay(
                    post_id=post_id,
                    telegram_chat_id=customer.telegram_id,
                    keyword_matches=match_filter.keyword_match_result,
                )


@app.task
def send_message_to_telegram(*, post_id: int, telegram_chat_id: int, keyword_matches: list[str]):
    bot_sender = BotSenderService(bot=TeleBot(token=settings.TELEGRAM_BOT_TOKEN))
    post_repository = PostRepository()

    post = post_repository.get(id=post_id)
    images_url = [settings.DOMEN_NAME + image.image.url for image in post.images.all()]

    message_text = get_message_text(post.description, post.url, keyword_matches, post.group_name, post.group_url)

    send_message(bot_sender, telegram_chat_id, message_text, images_url)
