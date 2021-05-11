# -*- coding: utf-8 -*-
"""
Created by susy at 2021/5/3
"""
from dao.base import *
from functools import wraps
import traceback
import common
import datetime

logger = common.get_default_logger()


def __try_release_conn():
    if not db.is_closed():
        try:
            # db.manual_close()
            db.close()
            # db._close(db.connection())
        except Exception:
            logger.error("exe action failed.", exc_info=True)
    else:
        logger.debug("db is closed!")


def clean_wrap_db_for_session():
    __try_release_conn()


def query_wrap_db_for_session(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if db.is_closed():
            db.connect()
        return func(*args, **kwargs)
    return wrapper


def query_wrap_db_auto_close(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if db.is_closed():
            db.connect()
        try:
            return func(*args, **kwargs)
        except Exception as e:
            traceback.print_exc()
        finally:
            __try_release_conn()

    return wrapper


class MarketLoadMap(EmptyModel):
    id = PrimaryKeyField()

    ip = CharField(null=False, max_length=64)
    tag = CharField(null=False, max_length=64)
    target_file = CharField(null=False, max_length=128)
    status = IntegerField(null=False, default=0)
    updated_at = DateTimeField(default=datetime.datetime.now, constraints=db_update_field_sql())

    @classmethod
    def field_names(cls):
        return ["id", "ip", "tag", "target_file", "status", "updated_at"]

    class Meta:
        db_table = 'market_load_map'
        database = db
