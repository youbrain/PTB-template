#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3 as sql

from base_functions import *

''' Class for communication with database.db here '''


class DataBase:
    def __init__(self, db_file):
        self.__conn = sql.connect(db_file, check_same_thread=False)
        self.__cursor = self.__conn.cursor()

    def select(self, *args):
        self.__cursor.execute(*args)
        return self.__cursor.fetchone()

    def select_all(self, *args):
        self.__cursor.execute(*args)
        return self.__cursor.fetchall()

    def insert(self, *args):
        self.__cursor.execute(*args)
        self.__conn.commit()

    def insert_many(self, *args):
        self.__cursor.executemany(*args)
        self.__conn.commit()

    def update(self, *args):
        self.__cursor.execute(*args)
        self.__conn.commit()

    def delate(self, *args):
        self.__cursor.execute(*args)
        self.__conn.commit()

    def get_connection(self):
        return (self.__cursor, self.__conn)


db = DataBase(config['db_file'])
