# -*- coding: utf-8 -*-

"""Simple Bot to reply to Telegram messages.
This program is dedicated to the public domain under the CC0 license.
This Bot uses the Updater class to handle the bot.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


class Bot:
    # Define a few command handlers. These usually take the two arguments bot and
    # update. Error handlers also receive the raised TelegramError object in error.
    def handler_start(self, update):
        """Send a message when the command /start is issued."""
        update.message.reply_text('Hi!')

    def handler_help(self, update):
        """Send a message when the command /help is issued."""
        update.message.reply_text('Help!')

    def handler_echo(self, update):
        """Echo the user message."""
        update.message.reply_text(update.message.text)

    def handler_error(self, update, error):
        """Log Errors caused by Updates."""
        logger.warning('Update "%s" caused error "%s"', update, error)