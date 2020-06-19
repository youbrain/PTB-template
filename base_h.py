#!/usr/bin/env python
# -*- coding: utf-8 -*-
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup)

from base import *
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