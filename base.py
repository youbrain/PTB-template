#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from os import environ as evars
from os.path import (abspath, basename, dirname)
import requests
import traceback

from database import User


with open('values.json', encoding='utf-8') as file:
    jso = json.loads(file.read())
    txts = jso['texts']
    keybs = jso['keyboards']

with open('config.json', encoding='utf-8') as file:
    config = json.loads(file.read())\



def new_response(func):
    ''' decorator for all new updates'''
    def wrapper(*args, **kwargs):
        user = User.get(User.chat_id == args[0]._effective_chat.id)
        text = txts.get(func.__name__)
        keyb = keybs.get(func.__name__)

        if args[0].callback_query:
            data = args[0].callback_query.data.split('_')
        else:
            data = None

        if user.is_banned:
            args[1].bot.send_message(
                args[0]._effective_chat.id, txts['you_were_banned'])
            return

        # before
        return_values = func(*args, data, user, text, keyb, **kwargs)
        # after
        return return_values
    return wrapper


def error_handler(bot, error):
    ''' send error log to dev '''
    traceback_text = traceback.format_exc()

    proj_name = basename(dirname(abspath(__file__)))
    filename = proj_name + '.txt'

    url = f"https://api.telegram.org/bot{evars['bot_token']}/sendDocument?chat_id={evars['dev_chat_id']}"

    if not any(err in traceback_text for err in config['ignore_errs']):
        with open(filename, 'w') as file:
            file.write(traceback_text)

        with open(filename, 'rb') as file:
            requests.post(url, files={'document': file})
