import re

from django.template.loader import get_template

from apps.common.models import Keyword


def find_phone_numbers(text) -> list[str]:
    phone_pattern = r"\+?\d{1,3}\s?\(?\d{1,4}\)?[\s.-]?\d{1,4}[\s.-]?\d{2,4}[\s.-]?\d{2,4}"

    phone_numbers = re.findall(phone_pattern, text)

    cleaned_numbers = []

    for number in phone_numbers:
        cleaned_number = re.sub(r"\D", "", number)
        cleaned_numbers.append(cleaned_number)

    return cleaned_numbers


def truncate_text(text: str, limit=600) -> str:
    if len(text) > limit:
        return text[:limit] + "..."
    return text


def get_message_text(message: str, post_url: str, keywords: list[Keyword], group_name: str, group_link: str) -> str:
    phone_numbers = find_phone_numbers(message)
    phone_number = phone_numbers[0] if phone_numbers else None

    keywords = list(map(lambda x: x.replace(" ", "_"), keywords))
    message = truncate_text(message, limit=600)

    context = {
        "message": message,
        "phone_number": phone_number,
        "advert_link": post_url,
        "keywords": keywords,
        "group_name": group_name,
        "group_link": group_link,
    }

    template = get_template("posts/telegram_message_template.html")
    message = template.render(context)

    return message
