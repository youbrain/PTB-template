#!/usr/bin/env python
# -*- coding: utf-8 -*-
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup)

from base_functions import *
from database import db

from functions import *
from handlers import *


''' Base bot's functionality (/start, /info handlers) here '''


''' COMMANDS HANDLERS '''


def info(update, context):
    update.message.reply_text(texts['info_c'])


def start(update, context):
    out = db.select(f"SELECT * FROM users WHERE chat_id={update.message.chat.id}")

    if not out:
        db.insert_many("INSERT INTO users (chat_id, first_name, username, last_name) VALUES (?, ?, ?, ?)",
                       ((update.message.chat.id, update.message.chat.first_name,
                         update.message.chat.username, update.message.chat.last_name)))
        update.message.reply_text(texts['welcome'])
    else:
        to_main(update, context)


def to_main(update, context):
    '''EXITING FROM ALL HANDLERS. TO BOT'S MAIN MENU'''
    update.message.reply_text(texts['to_main'],
                              reply_markup=ReplyKeyboardMarkup(keyboards['main'], resize_keyboard=True))
    return -1
