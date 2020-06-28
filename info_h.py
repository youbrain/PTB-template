#!/usr/bin/env python
# -*- coding: utf-8 -*-
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup)

from base_h import (to_main, new_update)
from functions import remove_keyboard
from base import (INFO_MAIN, texts, keyboards, config)



@new_update
def info_c(update, context):
	txt = update.message.text.split()

	if len(txt) == 2:
		user_p = User.get(User.chat_id == update._effective_chat.id)

		if user_p.is_oper or user_p.is_admin or user_p.is_owner:
			user = User.get_or_none(User.chat_id == txt[1])
			if user:
				if user.is_owner:
					bug_report_btn = InlineKeyboardButton(keyboards['bug_rep']['to'], callback_data='bug_report')
					update.message.reply_text(texts['info_c'], reply_markup=InlineKeyboardMarkup(((bug_report_btn, ), )))
					return

				keyb = get_n_column_keyb(get_inf_keyb(user, user_p), config['user_info_btns_per_line'])

				update.message.reply_text(get_user_info(user.chat_id), reply_markup=InlineKeyboardMarkup(keyb))

			else:
				update.message.reply_text(texts['info']['404'])
		else:
			bug_report_btn = InlineKeyboardButton(keyboards['bug_rep']['to'], callback_data='bug_report')
			update.message.reply_text(texts['info_c'], reply_markup=InlineKeyboardMarkup(((bug_report_btn, ), )))

	else:
		bug_report_btn = InlineKeyboardButton(keyboards['bug_rep']['to'], callback_data='bug_report')
		update.message.reply_text(texts['info_c'], reply_markup=InlineKeyboardMarkup(((bug_report_btn, ), )))



def to_info_screen(update, context):
	context.bot.send_message(update._effective_chat.id, texts['info']['menu'], reply_markup=ReplyKeyboardMarkup(keyboards['info_creen'], resize_keyboard=True, one_time_keyboard=True))
	if update.callback_query:
		update.callback_query.answer()
		update.callback_query.edit_message_reply_markup(reply_markup=None)
	return INFO_MAIN


def support(update, context):
	1
	# bug_report_btn = InlineKeyboardButton(keyboards['bug_rep']['to'], callback_data='bug_report')
 #	update.message.reply_text(texts['bug_report']['txt'], reply_markup=InlineKeyboardMarkup(((bug_report_btn, ), )))

def contacts(update, context):
	link = InlineKeyboardButton(config['contact'][0], url=config['contact'][1])
	back = InlineKeyboardButton(keyboards['info']['back'], callback_data='to_info_screen')
	update.message.reply_text(texts['info']['contacts'], reply_markup=InlineKeyboardMarkup([[link], [back]]))


def license(update, context):
	back = InlineKeyboardButton(keyboards['info']['back'], callback_data='to_info_screen')
	update.message.reply_text(texts['info']['license'], reply_markup=InlineKeyboardMarkup([[back]]))


def donate(update, context):
	keyb = [[], []]
	back = InlineKeyboardButton(keyboards['info']['back'], callback_data='to_info_screen')
	for btn in config['donate'][:4]:
		keyb[0].append(InlineKeyboardButton(btn[0], url=btn[1]))

	for btn in config['donate'][4:]:
		keyb[1].append(InlineKeyboardButton(btn[0], url=btn[1]))

	keyb.append([back])
	update.message.reply_text(texts['info']['donate'], reply_markup=InlineKeyboardMarkup(keyb))


