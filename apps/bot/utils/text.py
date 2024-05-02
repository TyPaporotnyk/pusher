import re

from django.template.loader import get_template


def find_phone_numbers(text) -> list[str]:
    phone_pattern = r"\+?\d{1,3}\s?\(?\d{1,4}\)?[\s.-]?\d{1,4}[\s.-]?\d{2,4}[\s.-]?\d{2,4}"

    phone_numbers = re.findall(phone_pattern, text)

    cleaned_numbers = []

    for number in phone_numbers:
        cleaned_number = re.sub(r"\D", "", number)
        cleaned_numbers.append(cleaned_number)

    return cleaned_numbers


def get_advert_text(message: str, advert_link: str, keywords: list[str], group_name: str, group_link: str) -> str:
    phone_numbers = find_phone_numbers(message)
    phone_number = phone_numbers[0] if phone_numbers else None

    keywords = list(map(lambda x: x.replace(" ", ""), keywords))

    context = {
        "message": message,
        "phone_number": phone_number,
        "advert_link": advert_link,
        "keywords": keywords,
        "group_name": group_name,
        "group_link": group_link,
    }

    template = get_template("bot/message/send_message.html")
    message = template.render(context)

    return message
