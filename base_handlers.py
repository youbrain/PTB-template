#!/usr/bin/env python
# -*- coding: utf-8 -*-
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup)

from base_functions import *
from database import *

from functions import *
from handlers import *


''' Base bot's functionality (/start, /info handlers) here '''


''' COMMANDS HANDLERS '''


def info(update, context):
    update.message.reply_text(texts['info_c'])


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


def to_main(update, context):
    '''EXITING FROM ALL HANDLERS. TO BOT'S MAIN MENU'''
    update.message.reply_text(texts['to_main'],
                              reply_markup=ReplyKeyboardMarkup(keyboards['main'], resize_keyboard=True))
    return -1
