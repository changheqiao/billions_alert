# -*- coding: utf-8 -*-
"""
Created by susy at 2021/5/3
"""

from dao.models import *


def init_db():
    db.create_tables([MarketLoadMap], safe=True)
    print("Init database ok")


class BaseDao(object):

    @classmethod
    @query_wrap_db_auto_close
    def query_load_map(cls, ip, tag) -> list:
        mq = MarketLoadMap.select().where(MarketLoadMap.ip == ip, MarketLoadMap.tag == tag, MarketLoadMap.status == 0)
        rs = []
        if mq:
            for mlm in mq:
                rs.append(MarketLoadMap.to_dict(mlm, ["id", "status", "updated_at"]))
        return rs
