#!/usr/bin/env python
# -*- coding: utf-8 -*-

import peewee
import datetime

from base_functions import *

''' Class for communication with database.db here '''

db = peewee.SqliteDatabase(config['db_file'])


class User(peewee.Model):
    id = peewee.AutoField()

    chat_id = peewee.IntegerField()
    first_name = peewee.CharField()
    last_name = peewee.CharField(null=True)
    username = peewee.CharField(null=True, unique=True)

    start_time = peewee.DateField(default=datetime.date.today)

    class Meta:
        database = db
        db_table = 'users'


User.create_table()
