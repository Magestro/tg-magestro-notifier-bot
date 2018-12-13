#!/usr/bin/env python3.7

import os
import time

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from src import MainConfig
from src.parser import Onliner, Kvartirant
from src.storage.db import Flat
from src.telegram.bot import Bot


def main():
    bot = Bot()
    """Start the bot."""
    config = MainConfig(os.path.dirname(__file__) + "/main.json")
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


def parse_kvartirant(config: MainConfig, updater):
    parser = Kvartirant()

    for flat in parser.get_all():
        try:
            print("try to find: where: {}; extid: {}".format(Kvartirant.where, flat.external_id))
            flat = Flat().select().where((Flat.where == Kvartirant.where) & (Flat.external_id == flat.external_id)).get()
        except:
            pass

        if flat.id is None:
            try:
                result = updater.bot.send_message(config.group_chat_id, "New flat from \"{}\" found!\n{}\n{}"
                                                  .format(flat.where, flat.address, flat.link) +
                                                  "\nprice: {}р.\nowner: {}\ncreated: {}\n"
                                                  .format(flat.price, flat.owner, flat.created_at))
                time.sleep(10)  # todo max msg per time
                flat.save()
                print("save flat: {}".format(flat.id))
            except Exception as e:
                print("cant send message: {}; exception: {}".format(flat.external_id, e))
                pass


def parse_onliner(config: MainConfig, updater):
    parser = Onliner()

    for flat in parser.get_all():
        try:
            print("try to find: where: {}; extid: {}".format(Onliner.where, flat.external_id))
            flat = Flat().select().where((Flat.where == Onliner.where) & (Flat.external_id == flat.external_id)).get()
        except:
            pass

        if flat.id is None:
            try:
                result = updater.bot.send_photo(config.group_chat_id, flat.photo, "New flat from \"{}\" found!\n{}\n{}"
                                                .format(flat.where, flat.address, flat.link) +
                                                "\nprice: ${}\nowner: {}\ncreated: {}\n"
                                                .format(flat.price, flat.owner, flat.created_at))
                time.sleep(0.5)
                updater.bot.send_location(config.group_chat_id, flat.latitude, flat.longitude, False, result.message_id)
                flat.save()
                time.sleep(10)  # todo max msg per time
                print("save flat: {}".format(flat.id))
            except Exception:
                print("cant send message: {}".format(flat.external_id))
                pass


if __name__ == '__main__':
    config = MainConfig(os.getcwd() + "/volume/main.json")  # todo
    updater = Updater(config.token)
    # main()
    while True:
        try:
            parse_kvartirant(config, updater)
            parse_onliner(config, updater)
        except Exception as e:
            print("exception occurred: %s" % e)
        print("end iteration")
        time.sleep(1800)
