#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Developer: Alexander Machek [@youbrain]
from telegram import ParseMode
from telegram.ext import (Updater, Filters, Defaults)
from telegram.ext import (CommandHandler, MessageHandler, CallbackQueryHandler)

from base import config

from handlers import start



def main():
    updater = Updater(config['bot_token'],
                      defaults=Defaults(parse_mode=ParseMode.HTML),
                      use_context=True)
    dp = updater.dispatcher


    # commands
    dp.add_handler(CommandHandler('start', start))

    # Conversation handlers
    # dp.add_handler(dash_h)

    # errors
    # dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
