import re
import logging
import os

from telegram.ext import Updater, MessageHandler

from bot.config import BOT_NAME
from bot.filters import MentionFilter
from bot.commands import BotCommandHandler
from currency_parser import get_currency

logging.basicConfig(format='%(asctime)s %(name)s [%(levelname)s]: %(message)s', level=logging.INFO)
logger = logging.getLogger('galera_bot.run')

cmd_pattern = re.compile('@[A-z0-9]+ (\w+)')


def default_handler(bot, update):
    bot.send_message(update.message.chat_id, f'{update.message.from_user.name} I don\'t know.')


def pong(bot, update):
    bot.send_message(update.message.chat_id, f'{update.message.from_user.name} pong')


def currencies(bot, update):
    curr = '\n'.join(get_currency())
    message = f"{update.message.from_user.name}\nКурсы валют на сегодня (Покупка/Продажа):\n{curr}"
    bot.send_message(update.message.chat_id, message)


def handle_command(bot, update):
    cmd = cmd_pattern.match(update.message.text) and cmd_pattern.match(update.message.text).group(1)
    cmd_handler.handle(cmd, bot, update)


def main():
    token = os.getenv('GALERA_API_TOKEN')
    updater = Updater(token=token)
    dispatcher = updater.dispatcher
    message_handler = MessageHandler(MentionFilter(BOT_NAME), callback=handle_command)
    dispatcher.add_handler(message_handler)
    logger.info('Start bot.')
    updater.start_polling()


if __name__ == '__main__':
    cmd_handler = BotCommandHandler(default_handler)
    cmd_handler.add_command('ping', pong)
    cmd_handler.add_command('currencies', currencies)

    main()