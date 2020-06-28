#!/usr/bin/env python
# -*- coding: utf-8 -*-
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup)

from base import (config, texts, keyboards)
from functions import (get_user_info, get_n_column_keyb, remove_keyboard)
from database import User

from base_h import to_main, new_update


def chose_lang(update, context):
	data = [[lang, f"set_lang_{lang}_1"] for lang in config['avaliable_langesges']]
	keyb = InlineKeyboardMarkup(get_n_column_keyb(data, config['chose_lang_columns']))

	if update.callback_query:
		update.callback_query.edit_message_text(texts['start']['chose_one_of'], reply_markup=keyb)
	else:
		remove_keyboard(update, context)
		update.message.reply_text(texts['start']['chose_one_of'], reply_markup=keyb)