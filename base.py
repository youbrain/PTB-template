#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import logging


file = open('config.json', encoding='utf-8')
config = json.loads(file.read())

with open(config['texts_file'], encoding='utf-8') as file:
    jso = json.loads(file.read())
    texts = jso['texts']
    keyboards = jso['keyboards']

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def test_h(name, func):
    return MessageHandler(Filters.regex(f"^({name})$"), func)