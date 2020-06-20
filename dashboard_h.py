#!/usr/bin/env python
# -*- coding: utf-8 -*-
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup)
from datetime import datetime

from statistics import median
# from functions import (get_data, publication_preview, get_n_column_keyb, send_draft, get_user_info, remove_keyboard)
from base_h import to_main, new_update
from database import User, Dayly_statistic
from base import *
'''DASHBOARD SCREEN'''


@new_update
def statistics(update, context):
	# parsing db
	count_all = User.select().count()
	new_today = User.select().where(User.start_time == datetime.now().date()).count()
	b = Dayly_statistic.select().where(Dayly_statistic.day == datetime.now().date())
	b = [a.msgs_count for a in b]
	# middle_m_day = Dayly_statistic.select(Dayly_statistic.msgs_count).where(Dayly_statistic.day == datetime.now().date()).median()
	# formating txt
	# .replace('<n_d>', str(new_today))
	txt = texts['dashboard']['statistics']['txt'].replace('<a_c>', str(count_all)).replace('<m_d>', str(len(b))).replace('<dd>', str(median(b)))
	update.message.reply_text(txt, reply_markup=ReplyKeyboardMarkup(keyboards['dashboard']['statistics'][0], resize_keyboard=True))
	return DASH_STAT
