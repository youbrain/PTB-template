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
'''
from telegram import ParseMode
from telegram.ext import (Updater, Filters, Defaults)
from telegram.ext import (CommandHandler, MessageHandler, ConversationHandler, CallbackQueryHandler)

import base
from base_h import (to_main, to_dashboard, to_main_with_msg_del, check_other_text)

from commands_h import start
from dashboard_h import statistics
from start_h import chose_lang
from interview_h import (inter_1, inter_2, save_marks, interview_other)
from settings_h import (settings, set_sth, pswd, edit_pswd, set_lockation_txt, set_locatipn_geo, set_coords)
from bug_report_h import (bug_report, bugrep_text, report_other, rem_part_report, send_report)
from info_h import (info_c, to_info_screen, support, contacts, license, donate, access)


def btn_handler(name, func):
    return MessageHandler(Filters.regex(f"^({name})$"), func)

def empty(a, b):
    1

def main():
    '''ENTRY POINT'''
    updater = Updater(base.config['bot_token'], use_context=True, defaults=Defaults(parse_mode=ParseMode.HTML))
    dp = updater.dispatcher

    # Conversation Handlers
    bug_report_h = ConversationHandler( # BUG REPORT 
        entry_points=[CallbackQueryHandler(bug_report, pattern="bug_report")],
        states={
            base.SEND_BUGREP_TXT:   [CallbackQueryHandler(to_main_with_msg_del, pattern="bug_rep_cancel"), # cancel report
                                     MessageHandler(Filters.text, bugrep_text)], # get a report text

            base.SEND_BUGREP_OTHER: [CallbackQueryHandler(to_main_with_msg_del, pattern="bug_rep_cancel"), # cancel report
                                     CallbackQueryHandler(rem_part_report, pattern="bug_rep_delp_"), # remove part of report
                                     CallbackQueryHandler(send_report, pattern="bug_rep_send"), # send report
                                     MessageHandler(Filters.all, report_other)]
        },
        fallbacks=[],
        per_message=False
    )

    dash_h = ConversationHandler( # DASHBOARD 
        entry_points=[CommandHandler("dashboard", to_dashboard)],
        states={
            base.DASH_MAIN:   [btn_handler(base.keyboards['dashboard']['menu'][0][0], statistics)], # statistics btn

            base.DASH_STAT:   [btn_handler(base.keyboards['dashboard']['statistics'][0][0][0], to_dashboard)] # back
        },
        fallbacks=[],
        per_message=False
    )

    settings_h = ConversationHandler( # SETTINGS btn
        entry_points=[btn_handler(base.keyboards['main'][0][0], settings)],
        states={
            base.SETTINGS_MAIN: [CallbackQueryHandler(to_main_with_msg_del, pattern="to_main"),
                                 CallbackQueryHandler(set_sth, pattern="set_"),
                                 CallbackQueryHandler(pswd, pattern="pswd_")],

            base.SET_PSWD:      [MessageHandler(Filters.text, edit_pswd)],

            base.SET_LOCATION:  [MessageHandler(Filters.text, set_lockation_txt),
                                 MessageHandler(Filters.location, set_locatipn_geo),
                                 CallbackQueryHandler(set_coords, pattern="set_coords_")]
        },
        fallbacks=[],
        per_message=False
    )

    interview_h = ConversationHandler( # INTERVIEW
        entry_points=[CallbackQueryHandler(inter_1, pattern="interview_1_")],
        states={
            base.INTERVIEW:       [CallbackQueryHandler(to_main_with_msg_del, pattern="to_main_c"),
                                   CallbackQueryHandler(inter_2, pattern="interview_2_"),
                                   CallbackQueryHandler(save_marks, pattern="interview_save")],

            base.INTERVIEW_MORE:  [CallbackQueryHandler(save_marks, pattern="interview_save"),
                                   MessageHandler(Filters.text, interview_other)]
        },
        fallbacks=[],
        per_message=False
    )

    start_h = ConversationHandler( # START 
        entry_points=[CommandHandler('start', start)],
        states={
            base.START_IS_CORRECT:       [btn_handler(base.keyboards['start']['cor_lang'], to_main),
                                          btn_handler(base.keyboards['start']['not_cor_lang'], chose_lang)]
        },
        fallbacks=[],
        per_message=False
    )

    info_h = ConversationHandler( # INFO btn 
        entry_points=[btn_handler(base.keyboards['main'][0][1], to_info_screen)],
        states={
            base.INFO_MAIN:        [btn_handler(base.keyboards['info_creen'][1][1], contacts),
                                    btn_handler(base.keyboards['info_creen'][2][0], license),
                                    btn_handler(base.keyboards['info_creen'][2][1], donate),
                                    btn_handler(base.keyboards['info_creen'][3][0], to_main),
                                    CallbackQueryHandler(to_info_screen, pattern='to_info_screen'),
                                    MessageHandler(Filters.text, empty)]
        },
        fallbacks=[],
        per_message=False
    )

    conversations = (settings_h, dash_h, bug_report_h, info_h, interview_h, start_h)

    # commands
    dp.add_handler(CommandHandler("info", info_c))

    # Conversation handlers
    for handler in conversations:
        dp.add_handler(handler)

    dp.add_handler(CallbackQueryHandler(to_main_with_msg_del, pattern="to_main_c"))
    dp.add_handler(CallbackQueryHandler(set_sth, pattern="set_"))
    dp.add_handler(CallbackQueryHandler(access, pattern="access_"))
    dp.add_handler(CallbackQueryHandler(pswd, pattern="pswd_reset_1"))
    dp.add_handler(CallbackQueryHandler(to_main_with_msg_del, pattern=''))
    dp.add_handler(MessageHandler(Filters.text, check_other_text))

    # errors
    # dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
