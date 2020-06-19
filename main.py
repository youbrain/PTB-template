#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
DEFAULT TEMPLATE

STRUCTURE:
    - main.py               ~ (entry point) Setting all handlers/controllers, etc (current file)
    - base.py               ~ Reading values.json file, setting config, texts, keyboards, inline vars. (logger)
    - base_h.py             ~ Base bot's handlers (to_main, bug_report)
    - database.py           ~ peewee classes for communication with database

    - commands_h.py         ~ Defult commands handlers (/start, /info) (adding other commands here too)

    - functions.py          ~ Custom function for specific bot (scrapers, api wrappers, etc)
    - test_handlers.py      ~ Custom handlers for custom menus, commands, navigation (1 button hendler, for tests)

    - database.db           ~ SQLite database for dev process (Postgresql on production)
    - config.json           ~ All projects configs, api keys, tokens, etc
    - values.json           ~ All bot's texts and keyboards, for different languages

Developer: Alexander Machek [@youbrain]
Repository: https://github.com/s404s/bot_ecosystem/tree/dev/organaizer

TODO:
    - all dev tasks here
'''
from telegram import ParseMode
from telegram.ext import (Updater, Filters, Defaults)
from telegram.ext import (CommandHandler, MessageHandler, ConversationHandler, CallbackQueryHandler)

from base import *
from base_h import (to_main, to_main_with_msg_del)

from commands_h import (info, start)
from bug_report_h import (bug_report, bugrep_text, report_other, rem_part_report, send_report)

from test_handlers import (button)


def main():
    '''ENTRY POINT'''
    updater = Updater(config['bot_token'], use_context=True, defaults=Defaults(parse_mode=ParseMode.HTML))
    dp = updater.dispatcher

    # Conversation Handlers
    bug_report_h = ConversationHandler( # BUG REPORT 
        entry_points=[CallbackQueryHandler(bug_report, pattern="bug_report")],
        states={
            SEND_BUGREP_TXT:   [CallbackQueryHandler(to_main_with_msg_del, pattern="bug_rep_cancel"), # cancel report
                                MessageHandler(Filters.text, bugrep_text)], # get a report text

            SEND_BUGREP_OTHER: [CallbackQueryHandler(to_main_with_msg_del, pattern="bug_rep_cancel"), # cancel report
                                CallbackQueryHandler(rem_part_report, pattern="bug_rep_delp_"), # remove part of report
                                CallbackQueryHandler(send_report, pattern="bug_rep_send"), # send report
                                MessageHandler(Filters.all, report_other)]
        },
        fallbacks=[],
        per_message=False
    )
    dp.add_handler(bug_report_h)

    # main menu btn
    dp.add_handler(MessageHandler(Filters.regex(f"^({keyboards['main'][0][0]})$"), button))

    # commands
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("info", info))

    # errors
    # dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
