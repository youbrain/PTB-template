#!/usr/bin/env python
# -*- coding: utf-8 -*-
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup)

from functions import (get_data, publication_preview, get_n_column_keyb, send_draft, get_user_info, remove_keyboard)
from base_h import to_main
from database import User
from base import *
'''SEND REPORT SCREEN'''


def bug_report(update, context):
    # cancle report btn
    keyb = InlineKeyboardMarkup([[InlineKeyboardButton(keyboards['bug_rep']['cancel'], callback_data='bug_rep_cancel')]])
    update.callback_query.answer()
    # removing main menu markup
    remove_keyboard(update, context)
    update.callback_query.message.reply_text(texts['bug_report']['txt'], reply_markup=keyb)
    return SEND_BUGREP_TXT


def bugrep_text(update, context):
    # creating places to temporary save report parts 
    context.user_data['drafts'] = {'bug_rep': {'main_text': update.message.text}}
    context.user_data['drafts']['bug_rep'].update({'other': []})

    main_t = update.message.text

    # checking for max preview len (in chars) 
    if not len(main_t) < config['preview_chars']:
        main_t = main_t[:config['preview_chars']]

    txt = f"<b>{texts['bug_report']['prefix']}</b><i>{main_t}</i>\n"

    # send & cancel report btns
    keyb = [[InlineKeyboardButton(keyboards['bug_rep']['send'], callback_data='bug_rep_send'),
             InlineKeyboardButton(keyboards['bug_rep']['cancel'], callback_data='bug_rep_cancel')]]

    m_id = update.message.reply_text(txt + texts['bug_report']['postfix'], reply_markup=InlineKeyboardMarkup(keyb)).message_id
    # saving last msg id for removing on next step
    context.user_data['drafts']['bug_rep'].update({'last_msg_id': m_id})

    return SEND_BUGREP_OTHER


def report_other(update, context):
    # parsing update for different content types & saving into user_data
    get_data(update, context, 'bug_rep', text=True, photo=True, voice=True)

    # main report text preview
    main_t = context.user_data['drafts']['bug_rep']['main_text']
    
    # checking for max preview len (in chars) 
    if not len(main_t) < config['preview_chars']:
        main_t = main_t[:config['preview_chars']]

    txt = texts['bug_report']['prefix']+main_t

    # parsing user_data & updating report preview text
    txt += publication_preview(context.user_data['drafts']['bug_rep']['other'])
    # remove part of report keyb 
    keyb = [(keyboards['bug_rep']["del_part"].replace('<n>', str(n)), f"bug_rep_delp_{n}")
            for n in range(1, len(context.user_data['drafts']['bug_rep']['other']) + 1)]
    #creating 3 column keyboard from data
    keyb = get_n_column_keyb(keyb, 3)
    # send & cancel report btns
    keyb.append([InlineKeyboardButton(keyboards['bug_rep']['send'], callback_data='bug_rep_send'),
                 InlineKeyboardButton(keyboards['bug_rep']['cancel'], callback_data='bug_rep_cancel')])

    m_id = update.message.reply_text(txt, reply_markup=InlineKeyboardMarkup(keyb)).message_id
    # delating last msg from bot
    context.bot.delete_message(chat_id=update.message.chat_id, message_id=context.user_data['drafts']['bug_rep']['last_msg_id'])
    # saving new last msg id
    context.user_data['drafts']['bug_rep']['last_msg_id'] = m_id


def rem_part_report(update, context):
    data = update.callback_query.data.split('_')
    # delating report part from user_data
    del context.user_data['drafts']['bug_rep']['other'][int(data[3]) - 1]

    # reports main text preview
    main_t = context.user_data['drafts']['bug_rep']['main_text']
    
    # checking for max preview len (in chars) 
    if not len(main_t) < config['preview_chars']:
        main_t = main_t[:config['preview_chars']]

    txt = f"<b>{texts['bug_report']['prefix']}</b><i>{main_t}</i>\n"

    # parsing user_data & updating report preview text
    txt += publication_preview(context.user_data['drafts']['bug_rep']['other'])
    # remove part of report keyb 
    keyb = [(keyboards['bug_rep']["del_part"].replace('<n>', str(n)), f"bug_rep_delp_{n}")
            for n in range(1, len(context.user_data['drafts']['bug_rep']['other']) + 1)]
    #creating 3 column keyboard from data
    keyb = get_n_column_keyb(keyb, 3)
    # send & cancel report btns
    keyb.append([InlineKeyboardButton(keyboards['bug_rep']['send'], callback_data='bug_rep_send'),
                 InlineKeyboardButton(keyboards['bug_rep']['cancel'], callback_data='bug_rep_cancel')])

    # editing msg
    update.callback_query.edit_message_text(txt, reply_markup=InlineKeyboardMarkup(keyb))


def send_report(update, context):
    # selecting all recipients
    opers = User.select().where(User.is_oper)

    for oper in opers:
        # sending info about report sender with reports main text
        txt = get_user_info(update._effective_chat.id)+'\n'+texts['bug_report']['oper_new']+context.user_data['drafts']['bug_rep']['main_text']
        context.bot.send_message(chat_id=oper.chat_id, text=txt)

        for draft in context.user_data['drafts']['bug_rep']['other']:
            # sending other report part
            send_draft(context, draft, oper.chat_id)
    # thnx for report
    update.callback_query.edit_message_text(texts['bug_report']['thnx'])
    # to main menu
    return to_main(update, context)