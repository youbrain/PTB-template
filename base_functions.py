import json


'''Base functions, reading config.json. (function wrappers, values.json) here '''

file = open('config.json')
config = json.loads(file.read())

with open(config['texts_file']) as file:
    jso = json.loads(file.read())
    texts = jso['ru']['texts']
    keyboards = jso['ru']['keyboards']

from database import *
from functions import *
