#!/usr/bin/env python3

import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from src.telegram.bot import Bot
from src.config.main import MainConfig


def main():
    bot = Bot()
    """Start the bot."""
    config = MainConfig(os.path.dirname(__file__)+"/main.json")
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(config.token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different   commands - answer in Telegram
    dp.add_handler(CommandHandler("start", bot.handler_start))
    dp.add_handler(CommandHandler("help", bot.handler_help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, bot.handler_echo))

    # log all errors
    dp.add_error_handler(bot.handler_error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()