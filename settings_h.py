#!/usr/bin/env python
# -*- coding: utf-8 -*-
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup)
from datetime import datetime

from functions import (remove_keyboard, get_n_column_keyb)
from base_h import to_main
from database import User
from base import *

''' settings '''


def get_settings_keyb(user):
	if user.use_stickers:
		s = InlineKeyboardButton(keyboards['settings']['headlines']['stickers']+keyboards['settings']['status'][0], callback_data='set_stickers_0')
	else:
		s = InlineKeyboardButton(keyboards['settings']['headlines']['stickers']+keyboards['settings']['status'][1], callback_data='set_stickers_1')
	
	n = InlineKeyboardButton(keyboards['settings']['headlines']['notify']+str(user.notify_time)[:5], callback_data='set_notify')
	
	'''
	if user.:
		s = texts['settings'][''][0]
	else:
		s = texts['settings'][''][1]
	'''
	keyb = [[s], [n]]
	return keyb

def settings(update, context):
	user = User.get(User.chat_id == update._effective_chat.id)

	keyb = get_settings_keyb(user)
	keyb.append([InlineKeyboardButton(keyboards['settings']['back'], callback_data='to_main')])
	txt = texts['settings']['txt']
	remove_keyboard(update, context)

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

	elif data[1] == 'notify' and len(data) == 2:
		hours = ('00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23')
		data = [[f"{texts['settings']['hour']}{num}", f"set_notify_hour_{num}"] for num in hours]
		keyb = get_n_column_keyb(data, 4)
		update.callback_query.edit_message_text(texts['settings']['set_notify_hour'], reply_markup=InlineKeyboardMarkup(keyb))

	elif data[1] == 'notify':
		if data[2] == 'hour':
			d = []
			mins = ('00', '05', '10', '15', '30', '45', '50', '55')
			for m in mins:
				time = data[3]+':'+m
				d.append((texts['settings']['minute']+time, 'set_notify_'+time))
			keyb = get_n_column_keyb(d, 4)
			update.callback_query.edit_message_text(texts['settings']['set_notify_min'], reply_markup=InlineKeyboardMarkup(keyb))
		else:
			h, m = data[2].split(':')
			user = User.get(User.chat_id == update._effective_chat.id)
			user.notify_time = datetime.strptime(h+':'+m,"%H:%M").time()
			user.save()

			keyb = get_settings_keyb(user)
			keyb.append([InlineKeyboardButton(keyboards['settings']['back'], callback_data='to_main')])
			txt = texts['settings']['txt']

			update.callback_query.edit_message_text(txt, reply_markup=InlineKeyboardMarkup(keyb))
			return SETTINGS_MAIN

