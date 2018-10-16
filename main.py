#!/usr/bin/env python3

import os
import time

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from src.storage.flat import Flat
from src.telegram.bot import Bot
from src.config.main import MainConfig
from src.parser.onliner import Onliner


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
    # main()
    parser = Onliner()


    config = MainConfig(os.path.dirname(__file__)+"/main.json")

    updater = Updater(config.token)

    for flat in parser.get_all():
        dbflat = Flat().select().where(Flat.where=="onliner" and Flat.external_id == flat.external_id).get()
        if dbflat.id:
            print("find flat: {}".format(dbflat.id))
            pass
        else:
            flat.save()
            print("save flat: {}".format(flat.id))
            # updater.bot.send_message(config.group_chat_id, str(flat))
            time.sleep(0.5)
