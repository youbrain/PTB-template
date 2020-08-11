#!/usr/bin/env python
# -*- coding: utf-8 -*-
from telegram.ext import Filters, ConversationHandler


# DASHBOARD 
dash_h = ConversationHandler( 
    entry_points=[CommandHandler("dashboard", to_dashboard)],
    states={
        0:   [btn_handler(base.keyboards['dashboard']['menu'][0][0], statistics)], # statistics btn

        1:   [btn_handler(base.keyboards['dashboard']['statistics'][0][0][0], to_dashboard)] # back
    },
    fallbacks=[],
    per_message=False
)
