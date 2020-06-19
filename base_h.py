#!/usr/bin/env python
# -*- coding: utf-8 -*-
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup)

from base import *
from database import User
'''Base bot's handlers (to_main, bug_report)'''


def to_main(update, context):
    '''EXITING FROM ALL HANDLERS. TO BOT'S MAIN MENU'''
    keyb = ReplyKeyboardMarkup(keyboards['main'], resize_keyboard=True)
    try:
        update.message.reply_text(texts['to_main'], reply_markup=keyb)
    except AttributeError:
        # update.callback_query.message.delete()
        context.bot.send_message(update.callback_query.message.chat.id, texts['to_main'], reply_markup=keyb)
    return -1


def to_main_with_msg_del(update, context):
    update.callback_query.message.delete()
    return to_main(update, context)


def to_dashboard(update, context):
    # privileged user with user chat_id
    user = User.select().where((User.is_admin == 1) & (User.chat_id == update._effective_chat.id))
    # if user exists
    if user.exists():
        # to dashboard handler
        update.message.reply_text(texts['dashboard']['dashboard_main'], reply_markup=ReplyKeyboardMarkup(keyboards['dashboard']['menu'], resize_keyboard=True))
        return DASH_MAIN
    else:
        # to main menu
        if config['show_no_access_warning']:
            update.message.reply_text(texts['dashboard']['no_access'])
        return to_main(update, context)


def on_new_message(func):    
    def wrapper(*args, **kwargs):
        
        return_value = func(*args, **kwargs)
        return return_value
    return wrapper