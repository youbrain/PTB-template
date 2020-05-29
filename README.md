## Default template for telegram bot *(python-telegram-bot)*

**Developer**: Alexander Machek, [youbrain](t.me/youbrain)

### REQUIREMENTS
`pip install -r requirements.txt`

**Python**: 3.8.2

**Packages**:
- json
- configparser
- logging
- sqlite3
- python-telegram-bot

### STRUCTURE
|**FILE**					| DESRIPTION															 |
|---------------------------|------------------------------------------------------------------------|
|main.py               		|* (entry point) Settings all handlers/controllers, etc (current file)	*|
|base_functions.py    		|* Base functions, reading config.ini. (function wrappers, values.json)	*|
|base_handlers.py      		|* Base bot's functionality (/start, /info handlers)					*|
|database.py           		|* Class for communication with database.db 							*|
|functions.py          		|* Custom function for specific bot (scrapers, api wrappers, etc)		*|
|handlers.py           		|* Custom handlers for custom menus, commands, navigation				*|
|database.db           		|* SQLite database for dev process (Postgresql on production)			*|
|config.ini            		|* All projects configs, api keys, tokens, etc							*|
|values.json           		|* All bot's texts and keyboards, for different languages				*|
