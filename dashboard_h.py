#!/usr/bin/env python
# -*- coding: utf-8 -*-
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup)

# from functions import (get_data, publication_preview, get_n_column_keyb, send_draft, get_user_info, remove_keyboard)
from base_h import to_main
from database import User
from base import *
'''DASHBOARD SCREEN'''


def statistics(update, context):
	# parsing db
	count_all = User.select().count()
	# formating txt
	txt = texts['dashboard']['statistics']['txt'].replace('<a_c>', str(count_all))
	update.message.reply_text(txt, reply_markup=ReplyKeyboardMarkup(keyboards['dashboard']['statistics'][0], resize_keyboard=True))
	return DASH_STAT
