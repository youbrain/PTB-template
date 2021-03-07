# Template for telegram bot *(python-telegram-bot)*

[![dev](https://img.shields.io/badge/Developer-Alexander%20Macheck-yellow)](https://t.me/youbrain)

## Instalation
    git clone https://github.com/youbrain/PTB-template
    cd PTB-template
    pip install -r requirements.txt


## Environment Variables:

    bot_token
    debug

If `debug` is `True` set `dev_chat_id`

## Start

`py main.py` 


### STRUCTURE
|**FILE**                   | DESCRIPTION                                                                           |
|---------------------------|---------------------------------------------------------------------------------------|
|main.py                    |* (entry point) Setting all handlers/controllers, etc (current file)                  *|
|database.py                |* peewee classes for communication with database                                      *|
|config.json                |* All projects configs, api keys, tokens, etc                                         *|
|values.json                |* All bot's texts and keyboards                                                       *|

