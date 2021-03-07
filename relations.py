#!/usr/bin/env python
# -*- coding: utf-8 -*-
from handlers import *

command_handlers = {
    # 'command': handler_func,
    'start': start,
    'help': help_h
}

conversation_handlers = [
    # test_ch
]

button_handlers = {
    # 'btn_name': handler_func,
    'show help': help_h
}

callback_handlers = {
    # 'callback': handler_func,
}
