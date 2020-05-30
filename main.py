#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
DEFAULT TEMPLATE

STRUCTURE:
    - main.py               ~ (entry point) Settings all handlers/controllers, etc (current file)
    - base_functions.py     ~ Base functions, reading config.ini. (function wrappers, values.json)
    - base_handlers.py      ~ Base bot's functionality (/start, /info handlers)

    - database.py           ~ Class for communication with database.db 
    - functions.py          ~ Custom function for specific bot (scrapers, api wrappers, etc)
    - handlers.py           ~ Custom handlers for custom menus, commands, navigation

    - database.db           ~ SQLite database for dev process (Postgresql on production)
    - config.json            ~ All projects configs, api keys, tokens, etc
    - values.json           ~ All bot's texts and keyboards, for different languages

Developer: Alexander Machek [@youbrain]
Repository: https://github.com/s404s/bot_ecosystem/tree/dev/organaizer

TODO:
    - all dev tasks here
'''
import logging
from telegram.ext import (Updater, Filters)
from telegram.ext import (CommandHandler, MessageHandler, ConversationHandler, CallbackQueryHandler)

from base_functions import *
from database import db
from base_handlers import *

from functions import *
from handlers import *


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    '''ENTRY POINT'''
    updater = Updater(config['bot_token'], use_context=True)
    dp = updater.dispatcher

    # main menu btn
    dp.add_handler(MessageHandler(Filters.regex(f"^({keyboards['main'][0][0]})$"), button))

    # commands
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("info", info))

    # callbacks
    # dp.add_handler(CallbackQueryHandler(del_callback, pattern="del_"))

    # Conversation Handlers
    # dp.add_handler(peopl_handler)

    # errors
    # dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
