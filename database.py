#!/usr/bin/env python
# -*- coding: utf-8 -*-
import peewee
from datetime import datetime
from os import environ as evars


'''
db = peewee.PostgresqlDatabase(
    'db_name',
    user='',
    password='',
    host='',
    port=5432,
    autocommit=True,
    autorollback=True
)
'''

db_file = 'development.db' if bool(evars['debug']) else 'production.db'
db = peewee.SqliteDatabase(db_file)


class User(peewee.Model):
    id = peewee.AutoField()
    chat_id = peewee.IntegerField()

    first_name = peewee.CharField()
    last_name = peewee.CharField(null=True)
    username = peewee.CharField(null=True, unique=True)
    language = peewee.CharField(null=True)
    start_time = peewee.DateTimeField(default=datetime.now())

    is_banned = peewee.BooleanField(default=False)

    class Meta:
        database = db
        db_table = 'users'


User.create_table()
