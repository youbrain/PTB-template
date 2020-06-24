## Default template for telegram bot *(python-telegram-bot)*

[![CodeFactor](https://www.codefactor.io/repository/github/youbrain/ptb_bot_template/badge)](https://www.codefactor.io/repository/github/youbrain/ptb_bot_template)

**Developer**: Alexander Machek, [youbrain](t.me/youbrain)

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
|base.py                    |* Reading values.json file, setting config, texts, keyboards, inline vars. (logger)   *|
|base_h.py                  |* Base bot's handlers (to_main, bug_report)                                           *|
|database.py                |* peewee classes for communication with database                                      *|
|commands_h.py              |* Defult commands handlers (/start, /info) (adding other commands here too)           *|
|functions.py               |* Custom function for specific bot (scrapers, api wrappers, etc)                      *|
|test_handlers.py           |* Custom handlers for custom menus, commands, navigation (1 button hendler, for tests)*|
|database.db           		|* SQLite database for dev process (Postgresql on production)			               *|
|config.json           		|* All projects configs, api keys, tokens, etc							               *|
|values.json           		|* All bot's texts and keyboards, for different languages				               *|
