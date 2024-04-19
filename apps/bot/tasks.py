from apps.bot.management.commands.bot import bot
from apps.bot.utils.broadcast import broadcast_group


def broadcast_group_task():
    broadcast_group(bot)


# def broadcast_keyword_task():
#     broadcast_keyword(bot)
