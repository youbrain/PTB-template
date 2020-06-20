#!/usr/bin/env python
# -*- coding: utf-8 -*-
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup)
from datetime import datetime, timedelta

from base import *
from blitz_h import blitz
from database import User, Dayly_statistic
'''Base bot's handlers (to_main, bug_report)'''


def new_update(func):    
    def wrapper(*args, **kwargs):
        now = Dayly_statistic.select().where(Dayly_statistic.day == datetime.now().date())
        if now:
            now[0].msgs_count += 1
            now[0].save()
        else: 
            Dayly_statistic.create(chat_id=args[0]._effective_chat.id).save()

        back_5 = datetime.now() - timedelta(days=config['blitz_throughout'])
        c = Dayly_statistic.select().where(Dayly_statistic.day >= back_5).count()

        user = User.select().where(User.chat_id == args[0]._effective_chat.id)

        if c == config['blitz_throughout'] and not user.is_interview:
            user.is_interview = True
            user.save()
            return blitz(args[0], args[1])

        if now.last


        return_value = func(*args, **kwargs)
        return return_value
    return wrapper


@new_update
def to_main(update, context):
    '''EXITING FROM ALL HANDLERS. TO BOT'S MAIN MENU'''
    keyb = ReplyKeyboardMarkup(keyboards['main'], resize_keyboard=True)
    try:
        update.message.reply_text(texts['to_main'], reply_markup=keyb)
    except AttributeError:
        # update.callback_query.message.delete()
        context.bot.send_message(update.callback_query.message.chat.id, texts['to_main'], reply_markup=keyb)
    return -1


@new_update
def to_main_with_msg_del(update, context):
    update.callback_query.message.delete()
    return to_main(update, context)


@new_update
def to_dashboard(update, context):
    # privileged user with user chat_id
    user = User.select().where((User.is_admin == 1) & (User.chat_id == update._effective_chat.id))
    # if user exists
    if user.exists():
        # to dashboard handler
        update.message.reply_text(texts['dashboard']['dashboard_main'], reply_markup=ReplyKeyboardMarkup(keyboards['dashboard']['menu'], resize_keyboard=True))
        return DASH_MAIN
    else:
        # to main menu
        if config['show_no_access_warning']:
            update.message.reply_text(texts['dashboard']['no_access'])
        return to_main(update, context)
