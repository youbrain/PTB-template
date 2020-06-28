#!/usr/bin/env python
# -*- coding: utf-8 -*-
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup)

from base_h import (to_main, new_update)
from functions import (remove_keyboard, get_n_column_keyb, get_user_info)
from database import User
from base import (INFO_MAIN, texts, keyboards, config)



def get_inf_keyb(user, user_p):
    ban_btn, oper_btn, admin_btn = None, None, None

    if user.is_banned:
        ban_btn = (keyboards['info']['access_unban'], 'access_unban_'+str(user.chat_id))
    else:
        ban_btn = (keyboards['info']['access_ban'], 'access_ban_'+str(user.chat_id))

    if user_p.is_admin or user_p.is_owner:
        if not user.is_oper:
            oper_btn = (keyboards['info']['access_oper'], 'access_oper_'+str(user.chat_id))
        else:
            oper_btn = (keyboards['info']['access_unoper'], 'access_unoper_'+str(user.chat_id))

    if user_p.is_owner:
        if not user.is_admin:
            admin_btn = (keyboards['info']['access_admin'], 'access_admin_'+str(user.chat_id))
        else:
            admin_btn = (keyboards['info']['access_unadmin'], 'access_unadmin_'+str(user.chat_id))

    return [oper_btn, admin_btn, ban_btn]


def access(update, context):
    update.callback_query.answer()
    
    d = update.callback_query.data.split('_')
    user_p = User.get(User.chat_id == update._effective_chat.id)
    user = User.get(User.chat_id == d[2])

    if d[1] == 'unban':
        user.is_banned = False    
    elif d[1] == 'ban':
        user.is_banned = True
    elif d[1] == 'oper':
        user.is_oper = True
    elif d[1] == 'unoper':
        user.is_oper = False
    elif d[1] == 'admin':
        user.is_admin = True
    elif d[1] == 'unadmin':
        user.is_admin = False

    user.save()
    keyb = get_n_column_keyb(get_inf_keyb(user, user_p), config['user_info_btns_per_line'])
    update.callback_query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(keyb))



@new_update
def info_c(update, context):
	txt = update.message.text.split()

	if len(txt) == 2:
		# user_p - privileged user, user - user to get info about
		user_p = User.get(User.chat_id == update._effective_chat.id)
		if user_p.is_oper or user_p.is_admin or user_p.is_owner:
			user = User.get_or_none(User.chat_id == txt[1])
			if user:
				if user.is_owner and not user.chat_id == user_p.chat_id:
					# hiding info about user owner
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
 	# update.message.reply_text(texts['bug_report']['txt'], reply_markup=InlineKeyboardMarkup(((bug_report_btn, ), )))

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

	# spliting keyboard for parts
	for btn in config['donate'][:4]:
		keyb[0].append(InlineKeyboardButton(btn[0], url=btn[1]))

	for btn in config['donate'][4:]:
		keyb[1].append(InlineKeyboardButton(btn[0], url=btn[1]))

	keyb.append([back])
	update.message.reply_text(texts['info']['donate'], reply_markup=InlineKeyboardMarkup(keyb))


