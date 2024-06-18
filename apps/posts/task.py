from logging import getLogger

from django.conf import settings
from telebot import TeleBot

from apps.base.exceptions.files import DownloadFileException
from apps.base.services.bot import BotSenderService, send_message_to_telegram
from apps.base.services.files import download_file
from apps.customers.models import CustomerPost
from apps.customers.services import CustomerPostService, CustomerService
from apps.filters.services.customer import CustomerPostMatchFilter
from apps.posts.repository import PostRepository
from apps.posts.utils.template import get_message_text
from config.celery import app

logger = getLogger(__name__)


@app.task
def link_post_to_users_task(post_id: int):
    post_repository = PostRepository()
    matched_users = 0

    post = post_repository.get(id=post_id)
    customers = CustomerService.get_all()

    for customer in customers:
        if (match_filter := CustomerPostMatchFilter(CustomerService(obj=customer))).is_valid(post):
            customer_post = CustomerPost(customer=customer, post=post)
            customer_post.save()

            customer_post.keywords.add(*match_filter.keyword_match_result)
            matched_users += 1
            logger.info(f"Linked post {post} to users {customer} by keywords: {match_filter.keyword_match_result}")

            if customer.telegram_id:
                send_message_to_telegram_task.delay(
                    customer_id=customer.id,
                    customer_post_id=customer_post.id,
                )

    return matched_users


@app.task
def send_message_to_telegram_task(
    *,
    customer_id: int,
    customer_post_id: int,
):
    bot_sender = BotSenderService(bot=TeleBot(token=settings.TELEGRAM_BOT_TOKEN))
    customer = CustomerService.get_by_id(customer_id)
    customer_post_service = CustomerPostService(obj=customer)

    customer_post = customer_post_service.get_by_id(customer_post_id)
    post = customer_post.post
    post_keywords = customer_post.keywords.all()
    post_images = post.images.all()

    image_urls = [image.original_image_url for image in post_images]

    message_text = get_message_text(post.description, post.url, post_keywords, post.group_name, post.group_url)

    send_message_to_telegram(bot_sender, customer.telegram_id, message_text, image_urls)

    logger.info(f"Sent post {post} to user {customer}")


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
            logger.warning(f"Cant download image {image_url} for post {post}")
