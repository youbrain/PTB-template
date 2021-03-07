#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
from telegram.ext import (Updater, Filters, Defaults)
from telegram.ext import (CommandHandler, MessageHandler,
                          ConversationHandler, CallbackQueryHandler)
                          
r_link = ConversationHandler(
    entry_points=[CallbackQueryHandler(my_liks, pattern='my_liks')],
    states={
        15: [CallbackQueryHandler(wlink, pattern='wlink_'),
             CallbackQueryHandler(
            set_ref_link, pattern='setlinkto_'),
            CallbackQueryHandler(birshiset, pattern='setbirshi'),
            CallbackQueryHandler(profile, pattern='back_to_profile')],

        5: [CallbackQueryHandler(get_wallet, pattern='get_wallet_'),
            CallbackQueryHandler(profile, pattern='back_to_profile'),
            MessageHandler(Filters.text, get_link_w)],

        base.SET_L: [CallbackQueryHandler(profile, pattern='back_to_profile'),
                     MessageHandler(Filters.text, s_l)]
    },
    fallbacks=[CallbackQueryHandler(to_main_with_msg_del, pattern=''),
               MessageHandler(Filters.text, to_main)],
)

'''