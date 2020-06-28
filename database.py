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
    language = peewee.CharField(null=True)
    start_time = peewee.DateTimeField(default=datetime.now())

    is_oper = peewee.BooleanField(default=False)
    is_admin = peewee.BooleanField(default=False)
    is_banned = peewee.BooleanField(default=False)
    is_owner = peewee.BooleanField(default=False)
    is_interviewed = peewee.BooleanField(default=False)
    use_stickers = peewee.BooleanField(default=False)

    coordinates = peewee.CharField(null=True)
    coord_place = peewee.CharField(null=True)

    lock_time = peewee.IntegerField(default=5)
    password = peewee.CharField(null=True)

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
        # auto editing last msg time
        self.last_msg_time = datetime.now().time()
        return super(Dayly_statistic, self).save(*args, **kwargs)

    class Meta:
        database = db
        db_table = 'dayly_statistic'


class Feedback(peewee.Model):
    id = peewee.AutoField()
    chat_id = peewee.IntegerField()

    mark_1 = peewee.IntegerField()
    mark_2 = peewee.IntegerField(null=True)
    txt = peewee.TextField(null=True)

    class Meta:
        database = db
        db_table = 'feedbacks'


User.create_table()
Feedback.create_table()
Dayly_statistic.create_table()