## Default template for telegram bot *(python-telegram-bot)*

[![dev](https://img.shields.io/badge/Developer-Alexander%20Macheck-yellow)](https://t.me/youbrain)

### REQUIREMENTS
`pip install -r requirements.txt`

**Python**: 3.8.2

**Packages**:
- json
- logging
- peewee
- python-telegram-bot

### STRUCTURE
|**FILE**					| DESCRIPTION															                |
|---------------------------|---------------------------------------------------------------------------------------|
|main.py                    |* (entry point) Setting all handlers/controllers, etc (current file)                  *|
|base.py                    |* Reading jsons, texts, keyboards,	configs											   *|
|database.py                |* peewee classes for communication with database                                      *|
|functions.py               |* Different helpfull functions							                   			   *|
|database.db           		|* SQLite database for dev process (Postgresql on production)			               *|
|config.json           		|* All projects configs, api keys, tokens, etc							               *|
|values.json           		|* All bot's texts and keyboards										               *|
