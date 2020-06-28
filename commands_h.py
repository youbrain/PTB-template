#!/usr/bin/env python
# -*- coding: utf-8 -*-
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup)

from base import (config, texts, keyboards, START_IS_CORRECT)
from functions import (get_user_info, get_n_column_keyb)
from database import User

from base_h import to_main, new_update

'''Defult commands handlers (/start, /info) (adding other commands here too)'''


# @new_update
def start(update, context):
    out = User.select().where(User.chat_id == update.message.chat.id)
    if not out:
        user = User.create(chat_id=update.message.chat.id,
                    first_name=update.message.chat.first_name,
                    last_name=update.message.chat.last_name,
                    username=update.message.chat.username,
                    language=update.effective_user.language_code)

        if str(update.message.chat.id) == config['owner_id']:
            user.is_owner = True
        user.save()

        keyb = ReplyKeyboardMarkup([[keyboards['start']['cor_lang'], keyboards['start']['not_cor_lang']]], resize_keyboard=True)

        # update.message.reply_text(texts['welcome'])
        # to_main(update, context)
        update.message.reply_text(texts['start']['lang'].replace('<lang>', update.effective_user.language_code), reply_markup=keyb)
        return START_IS_CORRECT
    else:
        to_main(update, context)


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


@new_update
def info(update, context):
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


