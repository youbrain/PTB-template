#!/usr/bin/env python
# -*- coding: utf-8 -*-
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup)

from base_h import to_main
from database import User
from base import *

''' settings '''


def get_settings_keyb(user):
	if user.use_stickers:
		s = InlineKeyboardButton(keyboards['settings']['headlines']['stickers']+keyboards['settings']['status'][0], callback_data='set_stickers_0')
	else:
		s = InlineKeyboardButton(keyboards['settings']['headlines']['stickers']+keyboards['settings']['status'][1], callback_data='set_stickers_1')

	'''
	if user.:
		s = texts['settings'][''][0]
	else:
		s = texts['settings'][''][1]
	'''
	keyb = [[s]]
	return keyb

def settings(update, context):
	user = User.get(User.chat_id == update._effective_chat.id)

	keyb = get_settings_keyb(user)
	keyb.append([InlineKeyboardButton(keyboards['settings']['back'], callback_data='to_main')])
	txt = texts['settings']['txt']

	update.message.reply_text(txt, reply_markup=InlineKeyboardMarkup(keyb))
	return SETTINGS_MAIN


def set_sth(update, context):
	data = update.callback_query.data.split('_')
	if data[1] == 'stickers':
		if data[2] == '1':
			u = User.get(User.chat_id == update._effective_chat.id)
			u.use_stickers = 1
			u.save()
		else:
			u = User.get(User.chat_id == update._effective_chat.id)
			u.use_stickers = 0
			u.save()

		keyb = get_settings_keyb(u)
		keyb.append([InlineKeyboardButton(keyboards['settings']['back'], callback_data='to_main')])
		# update.callback_query.edit_message_text(texts['settings']['txt'], reply_markup=InlineKeyboardMarkup(keyb))
		update.callback_query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(keyb))