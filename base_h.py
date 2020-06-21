#!/usr/bin/env python
# -*- coding: utf-8 -*-
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup)
from datetime import datetime, timedelta

from base import *
from blitz_h import blitz
from functions import remove_keyboard
from database import User, Dayly_statistic
'''Base bot's handlers (to_main, bug_report)'''


def new_update(func):    
    def wrapper(*args, **kwargs):
        now = Dayly_statistic.select().where(Dayly_statistic.day == datetime.now().date())
        user = User.get(User.chat_id == args[0]._effective_chat.id)

        # is bot locked
        if is_locked(user, now):
            return lock_screen(args[0], args[1])

        # editing msg today count & last msg time
        if now:
            now[0].msgs_count += 1
            now[0].save()
        else: 
            Dayly_statistic.create(chat_id=args[0]._effective_chat.id).save()

        # is interviewed
        back_5 = datetime.now() - timedelta(days=config['blitz_throughout'])
        c = Dayly_statistic.select().where(Dayly_statistic.day >= back_5).count()

        # if c == config['blitz_throughout'] and not user.is_interviewed:
        #     user.is_interview = True
        #     user.save()
        #     return blitz(args[0], args[1])


        return_value = func(*args, **kwargs)
        return return_value
    return wrapper


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


''' LOCK SCREEN '''
def lock_screen(update, context):
    remove_keyboard(update, context)
    update.message.reply_text(texts['lock']['enter_pswd'])


def is_locked(user, now):
    deff = datetime.now() - timedelta(minutes=user.lock_time)
    if now[0].last_msg_time <= deff.time():
        return True
    else:
        return False


def check_other_text(update, context):
    user = User.get(User.chat_id == update._effective_chat.id)
    now = Dayly_statistic.select().where(Dayly_statistic.day == datetime.now().date())

    if is_locked(user, now):
        # if password correct
        if user.password == update.message.text:
            now = Dayly_statistic.select().where(Dayly_statistic.day == datetime.now().date())
            # last msg time edit
            if now:
                now[0].msgs_count += 1
                now[0].save()
            else: 
                Dayly_statistic.create(chat_id=update._effective_chat.id).save()

            update.message.reply_text(texts['lock']['unlocked'])
            return to_main(update, context)
        else:
            lock_screen(update, context)
            update.message.reply_text(texts['lock']['invalid'])
    else:
        return to_main(update, context)