from apps.bot.utils.ai import find_emails, find_phone_numbers


def get_advert_text(additional: str, advert_link: str) -> str:
    phone_numbers = find_phone_numbers(additional)
    emails = find_emails(additional)

    message = ""

    if phone_numbers:
        message += f"<b>Phone numbers:</b> {','.join(phone_numbers)}\n\n"

    if emails:
        message += f"<b>Emails:</b> {','.join(emails)}\n\n"

    message += f"{additional}\n\n"
    message += advert_link

    return message
