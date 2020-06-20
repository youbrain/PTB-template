#!/usr/bin/env python
# -*- coding: utf-8 -*-
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup)

from base import (config, texts, keyboards, logger)
from database import User

from base_h import to_main, new_update

'''Defult commands handlers (/start, /info) (adding other commands here too)'''


@new_update
def info(update, context):
    bug_report_btn = InlineKeyboardButton(keyboards['bug_rep']['to'], callback_data='bug_report')
    update.message.reply_text(texts['info_c'], reply_markup=InlineKeyboardMarkup(((bug_report_btn, ), )))


@new_update
def start(update, context):
    out = User.select().where(User.chat_id == update.message.chat.id)

    if not out:
        User.create(chat_id=update.message.chat.id,
                    first_name=update.message.chat.first_name,
                    last_name=update.message.chat.last_name,
                    username=update.message.chat.username).save()
        update.message.reply_text(texts['welcome'])
    else:
        to_main(update, context)
