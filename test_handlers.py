#!/usr/bin/env python
# -*- coding: utf-8 -*-
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup)

from base import (config, texts, keyboards, logger)
from base_h import new_update
''' Custom handlers for custom menus, commands, navigation here '''


@new_update
def button(update, context):
    update.message.reply_text(texts['btn_txt'])
