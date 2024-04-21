from apps.bot.texts import MESSAGE_LINK_TEXT
from apps.bot.utils.ai import find_emails, find_phone_numbers


def get_advert_text(additional: str, advert_link: str) -> str:
    phone_numbers = find_phone_numbers(additional)
    emails = find_emails(additional)

    message = ""

    if phone_numbers:
        message += f"{', '.join(phone_numbers)}\n\n"

    if emails:
        message += f"{', '.join(emails)}\n\n"

    message += f"{additional}\n\n"
    message += f"<a href='{advert_link}'>{MESSAGE_LINK_TEXT}</a>"

    return message
