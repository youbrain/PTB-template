#!/usr/bin/env python
# -*- coding: utf-8 -*-
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove,
                      InlineKeyboardButton, InlineKeyboardMarkup)

from base import (config, texts, keyboards)
from database import User



def to_main(update, context):
    '''EXITING FROM ALL HANDLERS. TO BOT'S MAIN MENU'''
    keyb = ReplyKeyboardMarkup([])
    # keyb = ReplyKeyboardMarkup(keyboards['main'], resize_keyboard=True, one_time_keyboard=True)
    context.bot.send_message(update._effective_chat.id, texts['global']['main_menu'], reply_markup=keyb)
    return -1


def to_main_call_del(update, context):
    # to main with msg delate
    update.callback_query.message.delete()
    to_main(update, context)
    return -1 


def to_dashboard(update, context):
    user = User.get_or_none((User.is_admin == 1) & (User.chat_id == update._effective_chat.id))
    # if user exists
    if user:
        # to dashboard handler
        keyb = ReplyKeyboardMarkup([])
        # keyb = ReplyKeyboardMarkup(keyboards['dashboard']['menu'], resize_keyboard=True)
        update.message.reply_text(texts['dash']['main'], reply_markup=keyb)
        return 0


def start(update, context):
    out = User.select().where(User.chat_id == update.message.chat.id)
    if not out:
        user = User.create(chat_id=update.message.chat.id,
                    first_name=update.message.chat.first_name,
                    last_name=update.message.chat.last_name,
                    username=update.message.chat.username,
                    language=update.effective_user.language_code)
        user.save()

        keyb = ReplyKeyboardMarkup([])
        # keyb = ReplyKeyboardMarkup(, resize_keyboard=True)
        update.message.reply_text(texts['global']['start'], reply_markup=keyb)
        to_main(update, context)
        return -1
    else:
        to_main(update, context)
