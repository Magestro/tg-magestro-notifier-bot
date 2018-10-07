#!/usr/bin/env python3

import os
import sys
from telegram.ext import Updater
from src.config.main import MainConfig

config = MainConfig(os.path.dirname(__file__)+"/main.json")

updater = Updater(config.token)

updater.bot.send_message(config.group_chat_id, ' '.join(map(str, sys.argv[1:])))
