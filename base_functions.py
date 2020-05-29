import json
import configparser

from functions import *

'''Base functions, reading config.ini. (function wrappers, values.json) here '''

config = configparser.ConfigParser()
config.read('config.ini')
config = config['DEFAULT']

from database import db

with open(config['texts_file']) as file:
    jso = json.loads(file.read())
    texts = jso['ru']['texts']
    keyboards = jso['ru']['keyboards']
