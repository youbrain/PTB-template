#!/usr/bin/env python
# -*- coding: utf-8 -*-
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton)
from telegram.error import BadRequest
from geopy.geocoders import Nominatim
from datetime import datetime
from geocoder import geonames

from functions import (remove_keyboard, get_n_column_keyb)
from base_h import to_main, new_update
from database import User
from base import *
''' settings '''


def get_settings_keyb(user):
	if user.use_stickers:
		s = InlineKeyboardButton(keyboards['settings']['headlines']['stickers']+keyboards['settings']['status'][0], callback_data='set_stickers_0')
	else:
		s = InlineKeyboardButton(keyboards['settings']['headlines']['stickers']+keyboards['settings']['status'][1], callback_data='set_stickers_1')
	
	n = InlineKeyboardButton(keyboards['settings']['headlines']['notify']+str(user.notify_time)[:5], callback_data='set_notify')

	if user.password:
		r = InlineKeyboardButton(keyboards['settings']['headlines']['pswd_reset'], callback_data='pswd_reset')
		p = InlineKeyboardButton(keyboards['settings']['headlines']['change_password'], callback_data='pswd_set')
		t_p = InlineKeyboardButton(keyboards['settings']['headlines']['lock_time'].replace('<t>', str(user.lock_time)), callback_data='set_locktime')
	else:
		p = InlineKeyboardButton(keyboards['settings']['headlines']['set_password'], callback_data='pswd_set')
		t_p = None

	if user.coordinates:
		geolocator = Nominatim(user_agent="bot")
		address = geolocator.reverse(user.coordinates, language='en').raw['address']

		if address.get('village'):
			address['city'] = address['village']
		elif address.get('town'):
			address['city'] = address['town']
		print(address)
		b = f"{address['city']}, {address['country']}"
		c = InlineKeyboardButton(keyboards['settings']['headlines']['location']+b, callback_data='set_location')# .address
	else:
		c = InlineKeyboardButton(keyboards['settings']['headlines']['location_set'], callback_data='set_location')
	'''
	if user.:
		s = texts['settings'][''][0]
	else:
		s = texts['settings'][''][1]
	'''
	if t_p:
		keyb = [[s], [n], [p, r], [t_p], [c]]
	else:
		keyb = [[s], [n], [p], [c]]

	return keyb


@new_update
def settings(update, context):
	user = User.get(User.chat_id == update._effective_chat.id)

	keyb = get_settings_keyb(user)
	keyb.append([InlineKeyboardButton(keyboards['settings']['back'], callback_data='to_main')])

	remove_keyboard(update, context)
	context.user_data['m_id'] = update.message.reply_text(texts['settings']['txt'], reply_markup=InlineKeyboardMarkup(keyb)).message_id
	return SETTINGS_MAIN


@new_update
def set_sth(update, context):
	update.callback_query.answer()
	data = update.callback_query.data.split('_')

	# set sticker
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

	# notify time
	elif data[1] == 'notify' and len(data) == 2:
		hours = texts['notify_hours']
		data = [[f"{texts['settings']['hour']}{num}", f"set_notify_hour_{num}"] for num in hours]
		keyb = get_n_column_keyb(data, config['notify_time_set_columns'])
		update.callback_query.edit_message_text(texts['settings']['set_notify_hour'], reply_markup=InlineKeyboardMarkup(keyb))

	# notify time
	elif data[1] == 'notify':
		if data[2] == 'hour':
			d = []
			mins = texts['notify_mins']
			for m in mins:
				time = data[3]+':'+m
				d.append((texts['settings']['minute']+time, 'set_notify_'+time))
			keyb = get_n_column_keyb(d, config['notify_time_set_columns'])
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

	# locktime change
	elif data[1] == 'locktime':
		if len(data) == 2:
			mins = texts['locktime']
			d = [[texts['settings']['locktime_mins']+a, 'set_locktime_'+a] for a in mins]
			keyb = get_n_column_keyb(d, config['locktime_set_columns'])

			update.callback_query.edit_message_text(texts['settings']['locktime'], reply_markup=InlineKeyboardMarkup(keyb))
		else:
			user = User.get(User.chat_id == update._effective_chat.id)
			user.lock_time = int(data[2])
			user.save()

			keyb = get_settings_keyb(user)
			keyb.append([InlineKeyboardButton(keyboards['settings']['back'], callback_data='to_main')])
			txt = texts['settings']['txt']

			update.callback_query.edit_message_text(txt, reply_markup=InlineKeyboardMarkup(keyb))

	# setting location
	elif data[1] == 'location':
		btn = ReplyKeyboardMarkup([[KeyboardButton(keyboards['settings']['send_location'], request_location=True)]], resize_keyboard=True)

		context.bot.delete_message(chat_id=update._effective_chat.id, message_id=context.user_data['m_id'])

		context.user_data['m_id'] = context.bot.send_message(update._effective_chat.id, texts['settings']['location'], reply_markup=btn).message_id
		return SET_LOCATION


# @new_update
def pswd(update, context):
	data = update.callback_query.data.split('_')
	if data[1] == 'set':
		idi = update.callback_query.edit_message_text(texts['settings']['set_pswd']).message_id
		context.user_data['m_id'] = idi
		return SET_PSWD

	elif data[1] == 'reset':
		user = User.get(User.chat_id == update._effective_chat.id)
		user.password = ''
		user.save()

		keyb = get_settings_keyb(user)
		keyb.append([InlineKeyboardButton(keyboards['settings']['back'], callback_data='to_main')])
		txt = texts['settings']['txt']

		if len(data) == 3:
			return to_main(update, context)
		else:
			update.callback_query.edit_message_text(txt, reply_markup=InlineKeyboardMarkup(keyb))



@new_update
def edit_pswd(update, context):
	m = update.message.text
	# min len
	if len(m) >= config['min_pswd_lenght']:
		# spaces
		if not ' ' in m:
			context.bot.delete_message(chat_id=update._effective_chat.id, message_id=update.message.message_id)
			context.bot.edit_message_text(chat_id=update._effective_chat.id, message_id=context.user_data['m_id'], text=texts['settings']['pswd_set'])

			user = User.get(User.chat_id == update._effective_chat.id)
			user.password = m
			user.save()

			keyb = get_settings_keyb(user)
			keyb.append([InlineKeyboardButton(keyboards['settings']['back'], callback_data='to_main')])

			update.message.reply_text(texts['settings']['txt'], reply_markup=InlineKeyboardMarkup(keyb))
			return SETTINGS_MAIN
		else:
			idi = update.message.reply_text(texts['settings']['pswd_no_spaces']).message_id
			context.user_data['m_id'] = idi
	else:
		idi = update.message.reply_text(texts['settings']['pswd_no_min_lenght']).message_id
		context.user_data['m_id'] = idi


def set_lockation_txt(update, context):
	try:
		context.bot.delete_message(chat_id=update._effective_chat.id, message_id=context.user_data['m_id'])
	except BadRequest:
		pass

	all_l = geonames(update.message.text,  maxRows=config['maxRows_location'], key=config['key_location'])
	btns = []

	for l in all_l:
		btns.append([InlineKeyboardButton(f"{l.address}, {l.country}", callback_data=f"set_coords_{l.lat}_{l.lng}")])
	if all_l:
		update.message.reply_text(texts['settings']['locations'], reply_markup=InlineKeyboardMarkup(btns))
	else:
		update.message.reply_text(texts['settings']['other_loc'])


def set_locatipn_geo(update, context):
	user = User.get(User.chat_id == update._effective_chat.id)
	user.coordinates = f"{update.message.location['latitude']}, {update.message.location['longitude']}"
	user.save()


	keyb = get_settings_keyb(user)
	keyb.append([InlineKeyboardButton(keyboards['settings']['back'], callback_data='to_main')])
	txt = texts['settings']['txt']

	context.bot.delete_message(chat_id=update._effective_chat.id, message_id=update.message.message_id)
	context.bot.delete_message(chat_id=update._effective_chat.id, message_id=context.user_data['m_id'])
	remove_keyboard(update, context)
	update.message.reply_text(txt, reply_markup=InlineKeyboardMarkup(keyb))


def set_coords(update, context):
	data = update.callback_query.data.split('_')

	user = User.get(User.chat_id == update._effective_chat.id)
	user.coordinates = f"{data[2]}, {data[3]}"
	user.save()


	keyb = get_settings_keyb(user)
	keyb.append([InlineKeyboardButton(keyboards['settings']['back'], callback_data='to_main')])
	txt = texts['settings']['txt']

	# context.bot.delete_message(chat_id=update._effective_chat.id, message_id=update.message.message_id)
	# context.bot.delete_message(chat_id=update._effective_chat.id, message_id=context.user_data['m_id'])
	update.callback_query.edit_message_text(txt, reply_markup=InlineKeyboardMarkup(keyb))

