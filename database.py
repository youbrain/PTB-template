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

    start_time = peewee.DateTimeField(default=datetime.now())

    is_oper = peewee.BooleanField(default=False)
    is_admin = peewee.BooleanField(default=False)
    is_interview = peewee.BooleanField(default=False)
    use_stickers = peewee.BooleanField(default=False)

    password = peewee.IntegerField()
    notify_time = peewee.TimeField(default=datetime.now().time())

    class Meta:
        database = db
        db_table = 'users'


class Dayly_statistic(peewee.Model):
    id = peewee.AutoField()

    chat_id = peewee.IntegerField()

    day = peewee.DateField(default=datetime.now().date())
    msgs_count = peewee.IntegerField(default=0)
    last_msg_time = peewee.TimeField(default=datetime.now().time())

    def save(self, *args, **kwargs):
        self.last_msg_time = datetime.now().time()
        return super(Dayly_statistic, self).save(*args, **kwargs)

    class Meta:
        database = db
        db_table = 'dayly_statistic'


Dayly_statistic.create_table()
User.create_table()