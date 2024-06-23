from logging import getLogger

from django.conf import settings
from telebot import TeleBot

from apps.base.exceptions.files import DownloadFileException
from apps.base.services.bot import BotSenderService, send_message_to_telegram
from apps.base.services.files import download_file
from apps.customers.services.customers import CustomerService
from apps.customers.services.posts import CustomerPostService
from apps.filters.services.customer import CustomerPostMatchFilter
from apps.posts.repository import PostRepository
from apps.posts.utils.template import get_message_text
from config.celery import app

logger = getLogger(__name__)


@app.task
def link_post_to_users_task(post_id: int) -> int:
    matched_users = 0

    post = PostRepository().get(id=post_id)
    if not post:
        logger.error(f"Post with id {post_id} not found.")
        return matched_users

    customers = CustomerService.get_all()
    for customer in customers:
        try:
            customer_post_service = CustomerPostService(customer=customer)
            match_filter = CustomerPostMatchFilter(CustomerService(customer=customer))
            if match_filter.is_valid(post):
                customer_post = customer_post_service.create(post, match_filter.keyword_match_result)
                matched_users += 1
                logger.info(f"Linked post {post} to user {customer} by keywords: {match_filter.keyword_match_result}")

                if customer.telegram_id:
                    send_message_to_telegram_task.delay(
                        customer_id=customer.id,
                        customer_post_id=customer_post.id,
                    )
        except Exception as e:
            logger.error(f"Error linking post {post} to customer {customer}: {e}")

    return matched_users


@app.task
def send_message_to_telegram_task(customer_id: int, customer_post_id: int):
    bot = TeleBot(token=settings.TELEGRAM_BOT_TOKEN)
    bot_sender = BotSenderService(bot=bot)
    customer = CustomerService.get(customer_id)
    customer_service = CustomerService(customer=customer)

    try:
        customer_post = customer_service.posts_service.get(customer_post_id)
        post = customer_post.post
        post_keywords = customer_post.keywords.all()
        post_images = post.images.all()
        image_urls = [image.original_image_url for image in post_images]

        message_text = get_message_text(post.description, post.url, post_keywords, post.group_name, post.group_url)
        send_message_to_telegram(bot_sender, customer_service.customer.telegram_id, message_text, image_urls)
        logger.info(f"Sent post {post} to user {customer_service.customer}")

    except Exception as e:
        logger.error(f"Error sending message to customer {customer_id} for post {customer_post_id}: {e}")


@app.task
def load_post_images_task(post_id: int):
    post_repository = PostRepository()
    post = post_repository.get(id=post_id)
    if not post:
        logger.error(f"Post with id {post_id} not found.")
        return

    post_images = post.images.all()
    for image in post_images:
        image_url = image.original_image_url
        try:
            image.image.save(*download_file(image_url))
            logger.info(f"Downloaded and saved image {image_url} for post {post}")
        except DownloadFileException:
            logger.warning(f"Can't download image {image_url} for post {post}")
