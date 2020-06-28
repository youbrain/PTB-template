#!/usr/bin/env python
# -*- coding: utf-8 -*-
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup)

from base import (config, texts, keyboards, START_IS_CORRECT)
from database import User

from base_h import to_main

'''Defult commands handlers (/start, /info) (adding other commands here too)'''


# @new_update
def start(update, context):
    out = User.select().where(User.chat_id == update.message.chat.id)
    if not out:
        user = User.create(chat_id=update.message.chat.id,
                    first_name=update.message.chat.first_name,
                    last_name=update.message.chat.last_name,
                    username=update.message.chat.username,
                    language=update.effective_user.language_code)

        if str(update.message.chat.id) == config['owner_id']:
            user.is_owner = True
        user.save()

        keyb = ReplyKeyboardMarkup([[keyboards['start']['cor_lang'], keyboards['start']['not_cor_lang']]], resize_keyboard=True)
        update.message.reply_text(texts['start']['lang'].replace('<lang>', update.effective_user.language_code), reply_markup=keyb)
        
        return START_IS_CORRECT
    else:
        to_main(update, context)


