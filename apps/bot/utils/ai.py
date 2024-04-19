import re


def find_phone_numbers(text) -> list[str]:
    # Регулярное выражение для поиска номеров телефонов
    phone_pattern = r"\+?\d{1,3}\s?\(?\d{1,4}\)?[\s.-]?\d{1,4}[\s.-]?\d{2,4}[\s.-]?\d{2,4}"

    # Поиск всех номеров телефонов в тексте
    phone_numbers = re.findall(phone_pattern, text)

    # Список для хранения исправленных номеров
    cleaned_numbers = []

    # Перебор найденных номеров
    for number in phone_numbers:
        # Удаление всех символов, кроме цифр и плюса
        cleaned_number = re.sub(r"\D", "", number)
        cleaned_numbers.append(cleaned_number)

    return cleaned_numbers


def find_emails(text):
    # Паттерн для поиска адресов электронной почты
    email_pattern = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b")

    # Ищем все совпадения в тексте
    matches = re.findall(email_pattern, text)

    return matches
