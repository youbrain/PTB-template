#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Developer: Alexander Machek
'''
from telegram import ParseMode
from telegram.ext import (
    Updater,
    Filters,
    Defaults
)
from telegram.ext import (
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler
)

from base import evars, error_handler
from relations import (
    command_handlers,
    conversation_handlers,
    button_handlers,
    callback_handlers
)


def main():
    updater = Updater(
        evars['bot_token'],
        defaults=Defaults(parse_mode=ParseMode.HTML),
        use_context=True
    )

    # Adding all handlers from relations.py
    for handler in conversation_handlers:
        updater.dispatcher.add_handler(handler)

    for handler in command_handlers.items():
        updater.dispatcher.add_handler(
            CommandHandler(*handler)
        )

    for handler in button_handlers.items():
        updater.dispatcher.add_handler(
            MessageHandler(
                Filters.regex(f"^({handler[0]})$"),
                handler[1]
            )
        )

    for handler in callback_handlers.items():
        updater.dispatcher.add_handler(
            CallbackQueryHandler(handler[1], pattern=handler[0])
        )

    if bool(evars['debug']) is False:
        updater.dispatcher.add_error_handler(error_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
