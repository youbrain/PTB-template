#!/usr/bin/env python
# -*- coding: utf-8 -*-
import peewee
from datetime import datetime

from base import config

''' Class for communication with database.db here '''
db = peewee.SqliteDatabase(config['db_file'])


class User(peewee.Model):
    id = peewee.AutoField()

    chat_id = peewee.IntegerField()
    first_name = peewee.CharField()
    last_name = peewee.CharField(null=True)
    username = peewee.CharField(null=True, unique=True)

    start_time = peewee.DateTimeField(default=datetime.now)

    is_oper = peewee.BooleanField(default=False)

    class Meta:
        database = db
        db_table = 'users'


User.create_table()
