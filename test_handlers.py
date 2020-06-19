#!/usr/bin/env python
# -*- coding: utf-8 -*-
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup)

from base import (config, texts, keyboards, logger)
''' Custom handlers for custom menus, commands, navigation here '''


def button(update, context):
    update.message.reply_text(texts['btn_txt'])
