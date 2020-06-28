#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import logging
'''Reading values.json file, setting config, texts, keyboards, inline vars. (logger)'''


file = open('config.json')
config = json.loads(file.read())

with open(config['texts_file'], encoding='utf-8') as file:
    jso = json.loads(file.read())
    texts = jso['ru']['texts']
    keyboards = jso['ru']['keyboards']

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


''' STATES '''
# bug report
SEND_BUGREP_TXT, SEND_BUGREP_OTHER = range(2)

# dashboard
DASH_MAIN, DASH_STAT = range(2)

# settings
SETTINGS_MAIN, SET_PSWD, SET_LOCATION = range(3)

# lock
LOCK_PSWD = range(1)

# interview
INTERVIEW, INTERVIEW_MORE = range(2)

# start
START_IS_CORRECT = range(1)