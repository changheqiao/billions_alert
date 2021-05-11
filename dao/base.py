# -*- coding: utf-8 -*-
"""
Created by susy at 2021/5/3
"""
from peewee import *
from settings import mysql_config as config
from common import object_to_dict
import datetime

BATCH_DB_USER = config["user"]
BATCH_DB_PASSWORD = config["password"]
BATCH_DB_HOST = config["host"]
BATCH_DB_PORT = config["port"]
BATCH_DB_NAME = config["db"]

BATCH_DB_URL = 'mysql://%s:%s@%s:%s/%s' % (BATCH_DB_USER, BATCH_DB_PASSWORD, BATCH_DB_HOST, BATCH_DB_PORT,
                                           BATCH_DB_NAME)
BASE_FIELDS = ["created_at", "updated_at"]


def db_connect(url):
    # print("Use database : %s" % url)
    from playhouse.db_url import connect
    db = connect(url, False, **{"sql_mode": "traditional"})
    return db


try:
    db_exist = 'db' in locals() or 'db' in globals()
    if not db_exist:
        db = db_connect(BATCH_DB_URL)
        # db = RetryMySQLDatabase.db_instance()
        # print("db not exist.")
except Exception:
    db = db_connect(BATCH_DB_URL)


def db_create_field_sql():
    if BATCH_DB_URL.find("mysql") >= 0:
        return [SQL("DEFAULT current_timestamp")]
    else:
        return [SQL("DEFAULT (datetime('now'))")]


def db_update_field_sql():
    if BATCH_DB_URL.find("mysql") >= 0:
        return [SQL("DEFAULT current_timestamp ON UPDATE CURRENT_TIMESTAMP")]
    else:
        return [SQL("DEFAULT (datetime('now'))")]


class EmptyModel(Model):
    class Meta:
        # print("db=%s" % db)
        database = db

    @classmethod
    def field_names(cls):
        return []

    @classmethod
    def to_dict(cls, instance, excludes=[]):
        return object_to_dict(instance, cls.field_names(), excludes)


class BaseModel(EmptyModel):
    created_at = DateTimeField(index=True, constraints=db_create_field_sql())
    updated_at = DateTimeField(default=datetime.datetime.now, constraints=db_update_field_sql())

    @classmethod
    def field_names(cls):
        return BASE_FIELDS
