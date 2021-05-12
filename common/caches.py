# -*- coding: utf-8 -*-
"""
Created by susy at 2020/8/20
"""
from common import singleton, get_now_ts
from common.resources import common_r as item_cache
from functools import wraps
import json
import logging
log = logging.getLogger("consumer")


def _get_from_cache(key):
    data_obj_json_str = item_cache.get(key)
    if not data_obj_json_str:
        return None
    data_obj = json.loads(data_obj_json_str)
    return data_obj.get('data', None)


def get_from_cache(key):
    return _get_from_cache(key)


def get_cache_timeout(key):
    data_obj_json_str = item_cache.get(key)
    if not data_obj_json_str:
        return 0
    data_obj = json.loads(data_obj_json_str)
    return data_obj.get('to', 0)


def _put_to_cache(key, val, timeout_seconds=0):

    data_obj = {'data': val, 'tm': get_now_ts(), 'to': timeout_seconds, 'key': key}
    # DATA_CACHES[key] = data_obj
    data_obj_json_str = json.dumps(data_obj)
    log.debug("_put_to_cache key:{}, val:{}".format(key, data_obj_json_str))
    if timeout_seconds > 0:

        item_cache.set(key, data_obj_json_str, ex=timeout_seconds)
    else:
        item_cache.set(key, data_obj_json_str)


def put_to_cache(key, val, timeout_seconds=0):
    _put_to_cache(key, val, timeout_seconds)


def del_cache_data(cache_key):
    item_cache.delete(cache_key)


def cache_data(cache_key, timeout_seconds=None, verify_key=None, auto_update=False):

    def cache_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if isinstance(cache_key, str):
                key = cache_key.format(*args)
            elif callable(cache_key):
                key = cache_key(*args, **kwargs)
            else:
                key = cache_key

            data = _get_from_cache(key)
            if data:
                ori_to = get_cache_timeout(key)
                if verify_key:
                    if type(data) is dict and verify_key in data:
                        log.debug("cache hit ok!")
                        if auto_update:
                            _put_to_cache(key, data, ori_to)
                        return data
                    elif type(data) is object and hasattr(data, verify_key):
                        log.debug("cache hit ok!")
                        if auto_update:
                            _put_to_cache(key, data, ori_to)
                        return data
                else:
                    log.debug("cache hit ok!")
                    if auto_update:
                        _put_to_cache(key, data, ori_to)
                    return data

            result = func(*args, **kwargs)
            if not result:
                return result
            if not timeout_seconds:
                to = 0
            elif callable(timeout_seconds):
                to = timeout_seconds(*args, result)
            elif isinstance(timeout_seconds, str):
                to = int(timeout_seconds)
            elif timeout_seconds:
                to = timeout_seconds
            else:
                to = 0
            _put_to_cache(key, result, to)
            return result
        return wrapper
    return cache_decorator


"""
from django.core.cache import caches
item_cache = caches['item']
key='training:store:51888'
item_cache.get(key)
"""
