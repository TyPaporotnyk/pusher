from logging import getLogger

from django.conf import settings
from telebot import TeleBot

from apps.base.exceptions.files import DownloadFileException
from apps.base.services.bot import BotSenderService, send_message_to_telegram
from apps.base.services.files import download_file
from apps.common.models import Keyword
from apps.customers.models import CustomerPost
from apps.customers.services import CustomerService
from apps.filters.services.customer import CustomerPostMatchFilter
from apps.posts.repository import PostRepository
from apps.posts.utils.template import get_message_text
from config.celery import app

logger = getLogger(__name__)


@app.task
def link_post_to_users_task(post_id: int):
    post_repository = PostRepository()

    post = post_repository.get(id=post_id)
    customers = CustomerService.get_all_customers()

    for customer in customers:
        if (match_filter := CustomerPostMatchFilter(CustomerService(obj=customer))).is_valid(post):
            customer_post = CustomerPost(customer=customer, post=post)
            customer_post.save()

            customer_post.keywords.add(*match_filter.keyword_match_result)

            if customer.telegram_id:
                send_message_to_telegram_task.delay(
                    post_id=post_id,
                    telegram_chat_id=customer.telegram_id,
                    keyword_matches=match_filter.keyword_match_result,
                )


@app.task
def send_message_to_telegram_task(*, post_id: int, telegram_chat_id: int, keyword_matches: list[Keyword]):
    bot_sender = BotSenderService(bot=TeleBot(token=settings.TELEGRAM_BOT_TOKEN))
    post_repository = PostRepository()

    post = post_repository.get(id=post_id)
    post_images = post.images.all()

    image_urls = [image.original_image_url for image in post_images]

    message_text = get_message_text(post.description, post.url, keyword_matches, post.group_name, post.group_url)

    send_message_to_telegram(bot_sender, telegram_chat_id, message_text, image_urls)


@app.task
def load_post_images_task(*, post_id: int):
    post_repository = PostRepository()
    post = post_repository.get(id=post_id)
    post_images = post.images.all()

    for image in post_images:
        image_url = image.original_image_url
        try:
            image.image.save(*download_file(image_url))
        except DownloadFileException:
            logger.info("Cant download image: %s", image_url)
