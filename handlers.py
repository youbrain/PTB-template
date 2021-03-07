#!/usr/bin/env python
# -*- coding: utf-8 -*-
from telegram import ReplyKeyboardMarkup

from database import User
from base import new_response, txts, keybs


def start(update, context):
    user = User.get_or_none(User.chat_id == update.message.chat.id)
    if not user:
        # txt = update.message.text.split()
        # if len(txt) > 1:
        #     referal_code = update.message.text.replace('/start ', '')

        user = User.create(
            chat_id=update.message.chat.id,
            first_name=update.message.chat.first_name,
            last_name=update.message.chat.last_name,
            username=update.message.chat.username,
            language=update.effective_user.language_code
        )
        user.save()

    to_main(update, context)


@new_response
def to_main(update, context, data, user, text, keyb):
    context.bot.send_message(
        update._effective_chat.id,
        text,
        reply_markup=ReplyKeyboardMarkup(keyb)
    )


@new_response
def help_h(update, context, data, user, text, keyb):
    context.bot.send_message(
        update._effective_chat.id,
        text
    )
