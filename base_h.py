#!/usr/bin/env python
# -*- coding: utf-8 -*-
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup)
from telegram.error import BadRequest
from datetime import datetime, timedelta

from base import (config, texts, keyboards)
# from interview_h import interview
from functions import remove_keyboard
from database import User, Dayly_statistic
'''Base bot's handlers (to_main, bug_report)'''


def new_update(func):    
    def wrapper(*args, **kwargs):
        user = User.get(User.chat_id == args[0]._effective_chat.id)
        now = Dayly_statistic.select().where((Dayly_statistic.day == datetime.now().date())
                                       & (Dayly_statistic.chat_id == args[0]._effective_chat.id))

        if user.is_banned:
            args[1].bot.send_message(args[0]._effective_chat.id, texts['is_banned'])
            return

        # is bot locked
        if is_locked(user, now) and user.password:
            return lock_screen(args[0], args[1])

        # editing msg today count & last msg time
        if now:
            now[0].msgs_count += 1
            now[0].save()
        else: 
            Dayly_statistic.create(chat_id=args[0]._effective_chat.id).save()

        back = datetime.now() - timedelta(days=config['blitz_throughout'])

        days_wright = Dayly_statistic.select().where(Dayly_statistic.day >= back).count()

        # is interviewed
        if not user.is_interviewed and days_wright == config['blitz_throughout']:
            user.is_interviewed = True
            user.save()
            return to_interview(args[0], args[1])

        # run decorated function
        return_value = func(*args, **kwargs)
        return return_value
    return wrapper


@new_update
def to_main(update, context):
    '''EXITING FROM ALL HANDLERS. TO BOT'S MAIN MENU'''
    keyb = ReplyKeyboardMarkup(keyboards['main'], resize_keyboard=True, one_time_keyboard=True)

    if update.callback_query:
        context.bot.send_message(update.callback_query.message.chat.id, texts['to_main'], reply_markup=keyb)
    else:
        update.message.reply_text(texts['to_main'], reply_markup=keyb)

    return -1


def to_main_with_msg_del(update, context):
    # to main with msg delate
    update.callback_query.message.delete()
    return to_main(update, context)


@new_update
def to_dashboard(update, context):
    # privileged user with user chat_id
    user = User.select().where((User.is_admin == 1) & (User.chat_id == update._effective_chat.id))
    # if user exists
    if user.exists():
        # to dashboard handler
        keyb = ReplyKeyboardMarkup(keyboards['dashboard']['menu'], resize_keyboard=True)
        update.message.reply_text(texts['dashboard']['dashboard_main'], reply_markup=keyb)
        return DASH_MAIN
    else:
        # to main menu
        if config['show_no_access_warning']:
            update.message.reply_text(texts['dashboard']['no_access'])
        return to_main(update, context)


@new_update
def to_interview(update, context):
    keyb = [[InlineKeyboardButton(n, callback_data=f'interview_1_{n}') for n in range(1, config['marks_count'])]]
    keyb.append([InlineKeyboardButton(keyboards['interview']['skip'], callback_data='to_main_c')])

    context.bot.send_message(update._effective_chat.id, texts['interview']['mark'], reply_markup=InlineKeyboardMarkup(keyb))


''' LOCK SCREEN '''
def lock_screen(update, context):
    # context.bot.delete_message(chat_id=update._effective_chat.id, message_id=context.user_data['m_id'])
    keyb = InlineKeyboardMarkup([
            [InlineKeyboardButton(keyboards['settings']['headlines']['pswd_reset'], callback_data='pswd_reset_1')]
    ])
    msg = context.bot.send_message(update._effective_chat.id, texts['lock']['enter_pswd'], reply_markup=keyb)
    context.user_data['m_id'] = msg.message_id



def is_locked(user, now):
    if not now:
        return 0
    deff = datetime.now() - timedelta(minutes=user.lock_time)
    if now[0].last_msg_time <= deff.time():
        return True
    else:
        return False


def check_other_text(update, context):
    user = User.get(User.chat_id == update._effective_chat.id)
    now = Dayly_statistic.select().where(Dayly_statistic.day == datetime.now().date())

    if is_locked(user, now) and user.password:

        if context.user_data.get('m_id'):
            context.bot.delete_message(chat_id=update._effective_chat.id, message_id=context.user_data['m_id'])

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
    else:
        return to_main(update, context)