# -*- coding: utf-8 -*-
"""
Created by susy at 2020/10/14
"""
from common.resources import r
from common import utils_lock
import common
import settings
import time
import traceback
from typing import Callable

logger = common.get_default_logger()

ZSET_QUEUE_PREFIX = 'zs:q'
HSET_KEY_PREFIX = 'hs:q:t'


class RedisProducer(object):

    def __init__(self, name, max_len=10000):
        self.name = name
        self.queue_max_size = max_len
        self.zset_queue_name = "{}:{}".format(ZSET_QUEUE_PREFIX, name)

    def start(self):
        if not r.exists(self.name):
            self.push(dict(tag='hb'))
            t_list = r.xread({self.name: '0-0'}, 2, self.queue_max_size)
            if t_list:
                t = t_list[0]
                sn = common.to_str(t[0])
                datas = t[1]
                for i in range(len(datas)):
                    data = datas[i]
                    tid = common.to_str(data[0])
                    t_bd = common.to_str(data[1])

                    if t_bd:
                        tag = t_bd.get('tag', None)
                        if tag:
                            r.xdel(sn, tid)
                    # logger.debug('read streamname:{} tid:{} task:{}'.format(sn, tid, t_bd))

    def pool(self, item: dict):
        item_id = item.get('id', None)
        if item_id:
            lock_key = "lock:check:pool:{}".format(self.name)
            with utils_lock.CheckLock(lock_key):
                lock_put_pool_key = "lock:put:pool:{}".format(self.name)
                try:

                    utils_lock.redis_cache.set(name=lock_put_pool_key, value='1', nx=True, ex=10)

                    zkey = self.zset_queue_name
                    hs_key = "{}:{}".format(HSET_KEY_PREFIX, item_id)
                    plat_payload = common.plat_filter(item)
                    r.zadd(zkey, {hs_key: int((time.time()) * 1000)})
                    # if not r.exists(hs_key):
                    r.hset(hs_key, "tm", int(common.get_now_ts()), plat_payload)
                    # r.expire(hs_key, 24 * 60 * 60)
                    r.expire(hs_key, 10 * 60)
                except Exception:
                    traceback.print_exc()
                finally:
                    utils_lock.redis_cache.delete(lock_put_pool_key)

    def get_from_pool(self, item_id):
        if item_id:
            hs_key = item_id  # "{}:{}".format(HSET_KEY_PREFIX, item_id)
            return r.hgetall(hs_key)
        return None

    def check_pool_item(self, filter_item: Callable[[str, str], bool]=None, need_wait: Callable[[str, int, dict], None]=None,
                        consumer: Callable[[str, dict], bool]=None, progress: Callable[[int, int, int, int], None]=None,
                        complete: Callable[[int, int, int], None]=None):

        lock_key = "lock:check:pool:{}".format(self.name)
        if utils_lock.redis_cache.set(name=lock_key, value='1', nx=True, ex=10):
            lock_put_pool_key = "lock:put:pool:{}".format(self.name)

            try:
                with utils_lock.Lock(lock_put_pool_key):
                    key = self.zset_queue_name
                    now_timestamp = common.to_num(time.time() * 1000)
                    cnt = r.zcard(key)
                    if cnt > 0:
                        pool_items_set = r.zrange(key, 0, 0, withscores=True)
                        pool_item = pool_items_set[0]
                        item_id = common.to_str(pool_item[0])
                        start_at = common.to_num(pool_item[1])
                        if now_timestamp < start_at:
                            # timer_r.set(key, start_at, px=start_at - now_timestamp + 1)
                            if need_wait:
                                item_obj_dict = {}
                                item_obj = self.get_from_pool(item_id)
                                if item_obj:
                                    item_obj_dict = common.to_str(item_obj)
                                need_wait(item_id, start_at, item_obj_dict)
                        else:
                            has_next = True
                            dog = 10000
                            offset = 0
                            size = 100
                            ok_task_cnt = 0
                            while has_next and dog > 0:
                                dog = dog - 1
                                datas = r.zrangebyscore(key, 0, now_timestamp, start=offset, num=size)
                                n = len(datas)
                                offset = offset + size
                                has_next = n == size
                                ok_task_cnt = 0
                                if datas:
                                    last_item_id = None
                                    for _b_id in datas:
                                        item_id = common.to_str(_b_id)
                                        if filter_item:
                                            if filter_item(item_id, last_item_id):
                                                continue
                                        # to do
                                        if consumer:
                                            logger.debug("item_id:{}".format(item_id))
                                            item_obj = self.get_from_pool(item_id)
                                            if item_obj:
                                                item_obj_dict = common.to_str(item_obj)

                                                if consumer(item_id, item_obj_dict):
                                                    self.push(item_obj_dict)
                                            else:
                                                logger.debug("item_id:{}, can not get obj!".format(item_id))

                                        ok_task_cnt = ok_task_cnt + 1
                                        last_item_id = item_id
                                    r.zrem(key, *datas)
                                if progress and n > 0:
                                    progress(ok_task_cnt, n, offset-size, cnt)
                            if complete:
                                complete(ok_task_cnt, offset-size, cnt)
            except Exception:
                traceback.print_exc()
            finally:
                utils_lock.redis_cache.delete(lock_key)

    def push(self, item: dict):
        r.xadd(self.name, item, maxlen=self.queue_max_size)

    def length(self):
        return r.xlen(self.name)

    def pending_count(self, group_name):
        return r.xpending(self.name, group_name)

    def trim_half(self):
        if self.length() >= self.queue_max_size:
            r.xtrim(self.name, common.to_num(self.queue_max_size/2))
